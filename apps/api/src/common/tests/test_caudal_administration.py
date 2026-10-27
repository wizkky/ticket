"""Regression coverage for Chilean presentation and preserved admin permissions."""

import typing as t
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from django import forms
from django.contrib import admin
from django.test import Client, RequestFactory
from django.utils import timezone, translation

from accounts.models import RevelUser
from common.admin_localization import _choice_column
from common.money import round_currency_amount, valid_currency_precision
from common.service.invoice_utils import format_currency
from events.admin.ticket import PaymentAdmin, TicketTierAdmin
from events.models import Organization, Payment, TicketTier


@pytest.mark.parametrize("value,expected", [("0", "$0"), ("5000.00", "$5.000"), ("5500", "$5.500")])
def test_clp_formatting(value: str, expected: str) -> None:
    assert format_currency(Decimal(value), "CLP") == expected
    tier = TicketTier(price=Decimal(value), currency="CLP")
    assert TicketTierAdmin(TicketTier, admin.site).price_display(tier) == expected
    payment = Payment(amount=Decimal(value), currency="CLP")
    assert PaymentAdmin(Payment, admin.site).amount_display(payment) == expected


def test_historical_currency_and_percentages_are_preserved() -> None:
    tier = TicketTier(price=Decimal("12.50"), currency="EUR")
    assert TicketTierAdmin(TicketTier, admin.site).price_display(tier) == "€12.50"
    payment = Payment(amount=Decimal("5500"), currency="CLP", vat_amount=Decimal("1045"), vat_rate=Decimal("19.00"))
    assert PaymentAdmin(Payment, admin.site).vat_display(payment) == "$1.045 (19.00%)"


def test_fractional_pesos_rejected_and_discounts_rounded() -> None:
    assert valid_currency_precision(Decimal("5500"), "CLP")
    assert not valid_currency_precision(Decimal("5500.50"), "CLP")
    assert valid_currency_precision(Decimal("12.50"), "EUR")
    assert round_currency_amount(Decimal("5000.50"), "CLP") == Decimal("5001")


@pytest.mark.parametrize("month,offset", [(1, -3), (7, -4)])
def test_default_timezone_follows_chilean_daylight_saving(month: int, offset: int) -> None:
    assert str(timezone.get_default_timezone()) == "America/Santiago"
    stored = datetime(2026, month, 15, 22, 30, tzinfo=UTC)
    local = timezone.localtime(stored, timezone.get_default_timezone())
    assert local.hour == 22 + offset
    assert local.astimezone(UTC) == stored


def test_translated_choices_keep_stable_sorting_columns() -> None:
    with translation.override("es"):
        column = _choice_column("status", "Status")
        assert column is _choice_column("status", "Status")
        assert getattr(column, "admin_order_field") == "status"
        assert _choice_column("price_type", "Price type")(TicketTier()) == "Precio fijo"


@pytest.mark.django_db
def test_optional_models_hidden_but_authorized_history_accessible(
    client: Client, superuser: RevelUser, settings: t.Any
) -> None:
    settings.CAUDAL_SHOW_OPTIONAL_MODULES = False
    request = RequestFactory().get("/admin/")
    request.user = superuser
    hidden = {"ReferralCode", "PotluckItem", "TelegramUser", "MembershipSubscription"}
    visible = {model["object_name"] for app in admin.site.get_app_list(request) for model in app["models"]}
    assert not hidden.intersection(visible)
    assert "Ticket" in visible
    client.force_login(superuser)
    assert client.get("/admin/accounts/referralcode/").status_code == 200
    settings.CAUDAL_SHOW_OPTIONAL_MODULES = True
    restored = {model["object_name"] for app in admin.site.get_app_list(request) for model in app["models"]}
    assert hidden.issubset(restored)


@pytest.mark.django_db
def test_optional_inline_editors_hidden_and_saved_boolean_retained(superuser: RevelUser) -> None:
    request = RequestFactory().get("/admin/events/organization/add/")
    request.user = superuser
    model_admin = admin.site._registry[Organization]
    inline_names = {inline.model.__name__ for inline in model_admin.get_inlines(request)}
    assert "OrganizationStaff" in inline_names
    assert "OrganizationMember" not in inline_names
    assert "MembershipTier" not in inline_names
    field = model_admin.get_form(request).base_fields["accept_membership_requests"]
    assert isinstance(field.widget, forms.HiddenInput)
    assert field.clean(field.widget.value_from_datadict({"saved": "True"}, {}, "saved")) is True


@pytest.mark.django_db
def test_admin_remains_spanish_for_english_browser(client: Client, superuser: RevelUser) -> None:
    client.force_login(superuser)
    response = client.get("/admin/events/tickettier/", HTTP_ACCEPT_LANGUAGE="en-US")
    assert response.status_code == 200
    assert response.wsgi_request.LANGUAGE_CODE == "es"
    assert b'lang="es"' in response.content


@pytest.mark.django_db
def test_dashboard_initializes_charts_only_once(client: Client, superuser: RevelUser) -> None:
    client.force_login(superuser)
    response = client.get("/admin/")
    assert response.status_code == 200
    assert response.content.count(b"new Chart(userGrowthCtx") == 1
    assert b"grafana.letsrevel.io" not in response.content


@pytest.mark.django_db
def test_buyers_cannot_open_administration(client: Client, user: RevelUser) -> None:
    client.force_login(user)
    assert client.get("/admin/events/ticket/").status_code == 302


@pytest.mark.django_db
def test_retired_dietary_routes_are_absent(client: Client) -> None:
    assert client.get("/api/dietary/restrictions").status_code == 404
    assert client.get("/admin/accounts/dietaryrestriction/").status_code in (302, 404)
