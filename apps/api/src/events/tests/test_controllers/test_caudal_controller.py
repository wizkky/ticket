"""Caudal workspace boundaries and real operational counts."""

import pytest
from django.contrib.gis.geos import Point
from django.test.client import Client
from django.urls import reverse

from accounts.models import RevelUser
from events.filters import EventFilterSchema
from events.models import Event, Organization, OrganizationStaff, Ticket, TicketTier, Venue
from geo.models import City

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("name", ["caudal_workspace", "caudal_administration"])
def test_workspace_requires_authentication(client: Client, name: str) -> None:
    assert client.get(reverse(f"api:{name}")).status_code == 401


@pytest.mark.parametrize("fixture", ["organization_owner_client", "organization_staff_client", "nonmember_client"])
def test_platform_admin_is_not_a_producer(request: pytest.FixtureRequest, fixture: str) -> None:
    client = request.getfixturevalue(fixture)
    assert client.get(reverse("api:caudal_administration")).status_code == 403


def test_platform_admin_has_real_counts(superuser_client: Client, organization: Organization) -> None:
    response = superuser_client.get(reverse("api:caudal_administration"))
    assert response.status_code == 200
    sections = {section["key"]: section for section in response.json()["sections"]}
    assert sections["organizations"]["count"] == Organization.objects.count()
    assert sections["users"]["count"] == RevelUser.objects.count()
    assert sections["users"]["path"] == reverse("admin:accounts_reveluser_changelist")


def test_workspace_lists_only_actual_roles(
    organization_owner_client: Client, nonmember_client: Client, organization: Organization
) -> None:
    owned = organization_owner_client.get(reverse("api:caudal_workspace")).json()
    assert owned["platform_admin"] is False
    assert [org["id"] for org in owned["organizations"]] == [str(organization.id)]
    assert nonmember_client.get(reverse("api:caudal_workspace")).json()["organizations"] == []


def test_another_producer_cannot_read_metrics_or_door(
    nonmember_client: Client, organization: Organization, event: Event
) -> None:
    assert nonmember_client.get(
        reverse("api:caudal_producer_overview", kwargs={"slug": organization.slug})
    ).status_code in (403, 404)
    assert nonmember_client.get(reverse("api:caudal_door", kwargs={"event_id": event.id})).status_code == 403


def test_metrics_never_turn_door_reservations_into_online_payments(
    organization_owner_client: Client, organization: Organization, event: Event, organization_owner_user: RevelUser
) -> None:
    tier = event.ticket_tiers.first()
    assert tier is not None
    tier.payment_method = TicketTier.PaymentMethod.AT_THE_DOOR
    tier.price = 10
    tier.save()
    for status in [Ticket.TicketStatus.ACTIVE, Ticket.TicketStatus.PENDING, Ticket.TicketStatus.CHECKED_IN]:
        Ticket.objects.create(event=event, tier=tier, user=organization_owner_user, status=status)
    response = organization_owner_client.get(
        reverse("api:caudal_producer_overview", kwargs={"slug": organization.slug})
    )
    assert response.status_code == 200
    assert response.json()["metrics"] == {
        "issued": 2,
        "door_reservations": 3,
        "pending": 1,
        "admissions": 1,
        "online_payments": 0,
    }


def test_staff_permissions_are_rechecked_without_the_ui_permission_cache(
    organization_staff_client: Client, staff_member: OrganizationStaff, organization: Organization, event: Event
) -> None:
    staff_member.permissions = {"default": {"manage_tickets": True, "check_in_attendees": True}}
    staff_member.save()
    overview = reverse("api:caudal_producer_overview", kwargs={"slug": organization.slug})
    door = reverse("api:caudal_door", kwargs={"event_id": event.id})
    assert organization_staff_client.get(overview).json()["metrics"] is not None
    assert organization_staff_client.get(door).status_code == 200
    staff_member.permissions = {"default": {"manage_tickets": False, "check_in_attendees": False}}
    staff_member.save()
    assert organization_staff_client.get(overview).json()["metrics"] is None
    assert organization_staff_client.get(door).status_code == 403


def test_region_uses_the_venue_before_event_city_and_not_buyer_residence(event: Event) -> None:
    local = City.objects.create(
        name="Valdivia",
        ascii_name="Valdivia",
        country="Chile",
        iso2="CL",
        iso3="CHL",
        admin_name="Los Ríos",
        city_id=99000001,
        location=Point(-73.2459, -39.8142, srid=4326),
    )
    remote = City.objects.create(
        name="Santiago",
        ascii_name="Santiago",
        country="Chile",
        iso2="CL",
        iso3="CHL",
        admin_name="Metropolitana",
        city_id=99000002,
        location=Point(-70.6693, -33.4489, srid=4326),
    )
    event.city = local
    event.save(update_fields=["city"])
    filtered = EventFilterSchema(region="los-rios", next_events=False)
    assert filtered.filter(Event.objects.filter(pk=event.pk)).exists()
    venue = Venue.objects.create(organization=event.organization, name="Remote", city=remote)
    event.venue = venue
    event.save(update_fields=["venue"])
    assert not filtered.filter(Event.objects.filter(pk=event.pk)).exists()
    event.city = remote
    venue.city = local
    venue.save(update_fields=["city"])
    event.save(update_fields=["city"])
    assert filtered.filter(Event.objects.filter(pk=event.pk)).exists()
    assert (
        EventFilterSchema(region="los-rios", city_id=local.id, next_events=False)
        .filter(Event.objects.filter(pk=event.pk))
        .exists()
    )
