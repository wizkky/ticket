"""Permission-checked, read-only operations for the Caudal workspaces."""

from uuid import UUID

from django.db.models import Count, Q, QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja.errors import HttpError
from ninja_extra import api_controller, route

from accounts.models import RevelUser
from common.authentication import I18nJWTAuth
from events import models
from events.controllers.organization_admin.base import OrganizationAdminBaseController
from events.schema.caudal import (
    CaudalAdminOverview,
    CaudalAdminSection,
    CaudalEvent,
    CaudalMetrics,
    CaudalOrganization,
    CaudalProducerOverview,
    CaudalWorkspace,
)
from geo.models import City
from geo.schema import CitySchema


def ticket_metrics(tickets: QuerySet[models.Ticket]) -> CaudalMetrics:
    """Report operational counts; offline reservations never become online receipts."""
    active = Q(status__in=[models.Ticket.TicketStatus.ACTIVE, models.Ticket.TicketStatus.CHECKED_IN])
    counts = tickets.aggregate(
        issued=Count("pk", filter=active),
        door_reservations=Count(
            "pk",
            filter=Q(tier__payment_method=models.TicketTier.PaymentMethod.AT_THE_DOOR)
            & ~Q(status=models.Ticket.TicketStatus.CANCELLED),
        ),
        pending=Count("pk", filter=Q(status=models.Ticket.TicketStatus.PENDING)),
        admissions=Count("pk", filter=Q(status=models.Ticket.TicketStatus.CHECKED_IN)),
        online_payments=Count("pk", filter=Q(payment__status=models.Payment.PaymentStatus.SUCCEEDED)),
    )
    return CaudalMetrics(**counts)


@api_controller("/caudal", auth=I18nJWTAuth(), tags=["Caudal"])
class CaudalController(OrganizationAdminBaseController):
    @route.get("/cities", auth=None, response=list[CitySchema], url_name="caudal_cities")
    def cities(self) -> QuerySet[City]:
        """Existing locality records in Los Ríos, independent of a buyer's profile."""
        return (
            City.objects.filter(iso2="CL")
            .filter(Q(admin_name__icontains="Ríos") | Q(admin_name__icontains="Rios"))
            .order_by("name")
        )

    @route.get("/workspace", response=CaudalWorkspace, url_name="caudal_workspace")
    def workspace(self) -> CaudalWorkspace:
        """Only actual organization roles appear; platform access is independent."""
        user = self.user()
        organizations = models.Organization.objects.filter(Q(owner=user) | Q(staff_members=user)).distinct()
        return CaudalWorkspace(
            platform_admin=user.is_superuser,
            organizations=[
                CaudalOrganization(
                    id=org.id,
                    slug=org.slug,
                    name=org.name,
                    role="owner" if org.owner_id == user.id else "staff",
                )
                for org in organizations.order_by("name")
            ],
        )

    @route.get("/producer/{slug}", response=CaudalProducerOverview, url_name="caudal_producer_overview")
    def producer_overview(self, slug: str) -> CaudalProducerOverview:
        """Recheck membership and ticket permission on every request (no role cache)."""
        org = self.get_one(slug)
        if not org.is_owner_or_staff(self.user()):
            raise HttpError(403, "Organization access required")
        can_manage = org.has_org_permission(self.user().id, "manage_tickets")
        events = models.Event.objects.filter(organization=org, is_template=False).select_related("city", "venue__city")
        totals = events.count()
        events = events.annotate(
            issued_count=Count("tickets", filter=Q(tickets__status__in=["active", "checked_in"])),
            admission_count=Count("tickets", filter=Q(tickets__status="checked_in")),
        ).order_by("-start", "id")
        return CaudalProducerOverview(
            event_count=totals,
            metrics=ticket_metrics(models.Ticket.objects.filter(event__organization=org)) if can_manage else None,
            events=[
                CaudalEvent(
                    organization_slug=org.slug,
                    id=event.id,
                    name=event.name,
                    slug=event.slug,
                    start=event.start,
                    status=models.Event.EventStatus(event.status),
                    city=(
                        event.venue.city.name
                        if event.venue and event.venue.city
                        else event.city.name
                        if event.city
                        else None
                    ),
                    issued=int(getattr(event, "issued_count")) if can_manage else None,
                    admissions=int(getattr(event, "admission_count")) if can_manage else None,
                )
                for event in events[:12]
            ],
        )

    @route.get("/door/{event_id}", response=CaudalEvent, url_name="caudal_door")
    def door(self, event_id: UUID) -> CaudalEvent:
        """A dedicated door view checks the actual server-side check-in permission."""
        event = get_object_or_404(
            models.Event.objects.select_related("organization", "city", "venue__city"), pk=event_id
        )
        if not event.organization.has_org_permission(self.user().id, "check_in_attendees"):
            raise HttpError(403, "Check-in permission required")
        tickets = event.tickets.all()
        return CaudalEvent(
            organization_slug=event.organization.slug,
            id=event.id,
            name=event.name,
            slug=event.slug,
            start=event.start,
            status=models.Event.EventStatus(event.status),
            city=event.venue.city.name if event.venue and event.venue.city else event.city.name if event.city else None,
            issued=tickets.filter(status__in=["active", "checked_in"]).count(),
            admissions=tickets.filter(status="checked_in").count(),
        )

    @route.get("/administration", response=CaudalAdminOverview, url_name="caudal_administration")
    def administration(self) -> CaudalAdminOverview:
        """Global counts and existing Django management tools are superuser-only."""
        if not self.user().is_superuser:
            raise HttpError(403, "Platform administrator access required")
        organizations = models.Organization.objects.all()
        sections = [
            ("organizations", organizations.count(), "events_organization"),
            ("events", models.Event.objects.filter(is_template=False).count(), "events_event"),
            ("users", RevelUser.objects.count(), "accounts_reveluser"),
            ("tickets", models.Ticket.objects.count(), "events_ticket"),
        ]
        return CaudalAdminOverview(
            metrics=ticket_metrics(models.Ticket.objects.all()),
            sections=[
                CaudalAdminSection(key=key, count=count, path=reverse(f"admin:{model}_changelist"))
                for key, count, model in sections
            ],
            organizations=[
                CaudalOrganization(id=org.id, slug=org.slug, name=org.name, role="owner")
                for org in organizations.order_by("-created_at")[:8]
            ],
            producer_count=RevelUser.objects.filter(
                Q(owned_organizations__isnull=False) | Q(staff_organizations__isnull=False)
            )
            .distinct()
            .count(),
        )
