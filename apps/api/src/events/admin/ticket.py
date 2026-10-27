# src/events/admin/ticket.py
"""Admin classes for Ticket, TicketTier, and Payment models."""

import typing as t

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import AutocompleteSelectFilter

from common.admin_localization import ModelAdmin
from common.service.invoice_utils import format_currency
from events import models
from events.admin.base import (
    EventLinkMixin,
    UserLinkMixin,
    VenueLinkMixin,
)


@admin.register(models.TicketTier)
class TicketTierAdmin(ModelAdmin, EventLinkMixin, VenueLinkMixin):  # type: ignore[misc]
    """Admin view for TicketTier."""

    list_display = [
        "name",
        "event_link",
        "price_display",
        "price_type",
        "visibility",
        "payment_method",
        "quantity_display",
        "venue_link",
        "sector_name",
    ]
    list_select_related = ["event", "venue", "sector"]
    list_filter = [
        "visibility",
        "payment_method",
        "price_type",
        ("event", AutocompleteSelectFilter),
        ("venue", AutocompleteSelectFilter),
        ("sector", AutocompleteSelectFilter),
    ]
    list_filter_submit = True
    search_fields = ["name", "event__name", "description"]
    autocomplete_fields = ["event", "venue", "sector"]
    filter_horizontal = ["restricted_to_membership_tiers"]

    @admin.display(description=_("Price"), ordering="price")
    def price_display(self, obj: models.TicketTier) -> str:
        return format_currency(obj.price, obj.currency)

    @admin.display(description=_("Sold"), ordering="quantity_sold")
    def quantity_display(self, obj: models.TicketTier) -> str:
        total = obj.total_quantity if obj.total_quantity is not None else "∞"
        return f"{obj.quantity_sold} / {total}"

    @admin.display(description=_("Sector"))
    def sector_name(self, obj: models.TicketTier) -> str:
        return obj.sector.name if obj.sector else "—"


@admin.register(models.Ticket)
class TicketAdmin(ModelAdmin, UserLinkMixin, EventLinkMixin, VenueLinkMixin):  # type: ignore[misc]
    list_display = [
        "id",
        "event_link",
        "user_link",
        "tier_name",
        "venue_link",
        "sector_name",
        "seat_label",
        "status",
        "price_paid_display",
        "checked_in_at",
        "created_at",
    ]
    list_select_related = ["event", "user", "tier", "venue", "sector", "seat"]
    list_per_page = 50
    show_full_result_count = False
    list_filter = [
        "status",
        ("event", AutocompleteSelectFilter),
        ("tier", AutocompleteSelectFilter),
        ("venue", AutocompleteSelectFilter),
        ("sector", AutocompleteSelectFilter),
    ]
    list_filter_submit = True
    search_fields = ["event__name", "user__username", "user__email", "guest_name", "seat__label"]
    autocomplete_fields = ["event", "user", "tier", "checked_in_by", "venue", "sector", "seat"]
    readonly_fields = [
        "id",
        "checked_in_at",
        "checked_in_by",
        "price_paid",
        "discount_code",
        "discount_amount",
        "offline_refund_amount",
        "sale_source",
        "held_pass",
        "refund_policy_snapshot",
        "attribution",  # written once by checkout (#922); the export relies on it being an object
        "cancelled_at",
        "cancelled_by",
        "cancellation_source",
        "file_content_hash",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = [
        (None, {"fields": ["id", "event", "user", "guest_name", "status", "tier"]}),
        (_("Seating"), {"fields": ["venue", "sector", "seat"]}),
        (
            _("Payment & Discounts"),
            {
                "fields": [
                    "price_paid",
                    "discount_code",
                    "discount_amount",
                    "offline_refund_amount",
                    "sale_source",
                    "refund_policy_snapshot",
                    "held_pass",
                ]
            },
        ),
        (_("Check-in"), {"fields": ["checked_in_at", "checked_in_by"]}),
        (
            _("Cancellation"),
            {"fields": ["cancelled_at", "cancelled_by", "cancellation_source", "cancellation_reason"]},
        ),
        (_("Metadata"), {"fields": ["file_content_hash", "created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description=_("Price paid"), ordering="price_paid")
    def price_paid_display(self, obj: models.Ticket) -> str:
        return format_currency(obj.price_paid, obj.tier.currency) if obj.price_paid is not None and obj.tier else "—"

    @admin.display(description=_("Tier"))
    def tier_name(self, obj: models.Ticket) -> str | None:
        return obj.tier.name if obj.tier else "—"

    @admin.display(description=_("Sector"))
    def sector_name(self, obj: models.Ticket) -> str | None:
        return obj.sector.name if obj.sector else "—"

    @admin.display(description=_("Seat"))
    def seat_label(self, obj: models.Ticket) -> str | None:
        return obj.seat.label if obj.seat else "—"


@admin.register(models.Payment)
class PaymentAdmin(ModelAdmin, UserLinkMixin, EventLinkMixin):  # type: ignore[misc]
    """Admin for Payment model with financial tracking."""

    list_display = [
        "id_short",
        "user_link",
        "ticket_link",
        "amount_display",
        "vat_display",
        "platform_fee_display",
        "status_display",
        "stripe_session_id_short",
        "created_at",
    ]
    list_select_related = ["user", "ticket"]
    list_per_page = 50
    show_full_result_count = False
    # incident_hold_at is deliberately editable (not in readonly_fields): clearing it is
    # the operator resolution path for a stripe_session_total_mismatch hold (#756).
    list_filter = [
        "status",
        "refund_status",
        "currency",
        "created_at",
        "expires_at",
        ("incident_hold_at", admin.EmptyFieldListFilter),
    ]
    search_fields = ["user__username", "user__email", "ticket__event__name", "stripe_session_id"]
    readonly_fields = [
        "id",
        "user",
        "ticket",
        "amount",
        "currency",
        "platform_fee",
        "stripe_session_id",
        "stripe_payment_intent_id",
        "reservation_id",
        "raw_response",
        "net_amount",
        "vat_amount",
        "vat_rate",
        "platform_fee_net",
        "platform_fee_vat",
        "platform_fee_vat_rate",
        "platform_fee_reverse_charge",
        "buyer_billing_snapshot",
        "refund_amount",
        "refund_status",
        "stripe_refund_id",
        "refund_failure_reason",
        "refunded_at",
        "expires_at",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = [
        (None, {"fields": ["id", "user", "ticket", "status", "stripe_session_id"]}),
        (_("Amounts"), {"fields": ["amount", "currency", "net_amount", "vat_amount", "vat_rate"]}),
        (
            _("Platform Fee"),
            {
                "fields": [
                    "platform_fee",
                    "platform_fee_net",
                    "platform_fee_vat",
                    "platform_fee_vat_rate",
                    "platform_fee_reverse_charge",
                ]
            },
        ),
        (
            _("Refund"),
            {"fields": ["refund_status", "refund_amount", "stripe_refund_id", "refund_failure_reason", "refunded_at"]},
        ),
        (_("Billing Snapshot"), {"fields": ["buyer_billing_snapshot"], "classes": ["collapse"]}),
        (_("Stripe"), {"fields": ["stripe_payment_intent_id", "reservation_id", "raw_response"]}),
        (_("Dates"), {"fields": ["expires_at", "created_at", "updated_at"]}),
    ]

    @admin.display(description=_("ID"))
    def id_short(self, obj: models.Payment) -> str:
        return str(obj.id)[:8] + "..."

    @admin.display(description=_("Ticket"))
    def ticket_link(self, obj: models.Payment) -> str:
        url = reverse("admin:events_ticket_change", args=[obj.ticket.id])
        return format_html('<a href="{}">{}</a>', url, f"Ticket {str(obj.ticket.id)[:8]}...")

    @admin.display(description=_("Amount"))
    def amount_display(self, obj: models.Payment) -> str:
        return format_currency(obj.amount, obj.currency)

    @admin.display(description=_("Status"))
    def status_display(self, obj: models.Payment) -> str:
        colors: dict[t.Any, str] = {
            models.Payment.PaymentStatus.PENDING: "orange",
            models.Payment.PaymentStatus.SUCCEEDED: "green",
            models.Payment.PaymentStatus.FAILED: "red",
            models.Payment.PaymentStatus.REFUNDED: "blue",
        }
        color = colors.get(obj.status, "gray")
        return mark_safe(f'<span style="color: {color};">{obj.get_status_display()}</span>')

    @admin.display(description=_("VAT"))
    def vat_display(self, obj: models.Payment) -> str:
        if obj.vat_amount is not None:
            return f"{format_currency(obj.vat_amount, obj.currency)} ({obj.vat_rate}%)"
        return "—"

    @admin.display(description=_("P. Fee"))
    def platform_fee_display(self, obj: models.Payment) -> str:
        if obj.platform_fee_reverse_charge:
            return f"{format_currency(obj.platform_fee, obj.currency)} ({_('RC')})"
        if obj.platform_fee_net is not None:
            parts = [format_currency(obj.platform_fee, obj.currency)]
            if obj.platform_fee_vat:
                parts.append(f"{_('VAT')} {format_currency(obj.platform_fee_vat, obj.currency)}")
            return " / ".join(parts)
        if obj.platform_fee:
            return format_currency(obj.platform_fee, obj.currency)
        return "—"

    @admin.display(description=_("Stripe Session"))
    def stripe_session_id_short(self, obj: models.Payment) -> str:
        if obj.stripe_session_id:
            return obj.stripe_session_id[:20] + "..."
        return "-"
