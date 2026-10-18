#!/usr/bin/env python3
"""Create repeatable local Caudal fixtures without deleting application data.

Run with the backend's virtualenv: apps/api/.venv/bin/python scripts/seed_demo.py
Passwords are generated once and kept only in ignored .local/demo-credentials.json.
"""

from __future__ import annotations

import json
import os
import secrets
import sys
import typing as t
from datetime import timedelta
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"
CREDENTIALS_PATH = LOCAL / "demo-credentials.json"
MANIFEST_PATH = LOCAL / "demo.json"


def write_private_json(path: Path, content: t.Any) -> None:
    """Persist local fixture data with restrictive permissions, including on reruns."""
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.chmod(path, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(content, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def seed_demo() -> dict[str, t.Any]:
    """Use stable fixture IDs; preserve previous tickets, scans and passwords."""
    sys.path.insert(0, str(ROOT / "apps/api/src"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "revel.settings")

    import django
    from decouple import config

    django.setup()

    from accounts.models import RevelUser
    from django.conf import settings
    from django.contrib.gis.geos import Point
    from django.db import transaction
    from django.utils import timezone
    from events.models import DEFAULT_TICKET_TIER_NAME, Event, Organization, TicketTier
    from geo.models import City

    if not settings.DEBUG or not config("CAUDAL_DEMO", default=False, cast=bool):
        raise RuntimeError(
            "Los datos demo requieren DEBUG=True y CAUDAL_DEMO=True; no usar en producción."
        )

    credentials = (
        json.loads(CREDENTIALS_PATH.read_text()) if CREDENTIALS_PATH.exists() else {}
    )
    roles = {
        "producer_a": ("productor-a@caudal.example.com", "Productora", "Caudal"),
        "producer_b": ("productor-b@caudal.example.com", "Productor", "Independiente"),
        "buyer": ("comprador@caudal.example.com", "Compradora", "Demo"),
        "admin": ("admin@caudal.example.com", "Administración", "Caudal"),
    }
    # Persist passwords before DB creation so a partial seed can safely be resumed.
    for role, (email, _first_name, _last_name) in roles.items():
        credentials.setdefault(
            role, {"email": email, "password": secrets.token_urlsafe(24)}
        )
    write_private_json(CREDENTIALS_PATH, credentials)

    with transaction.atomic():
        users = {}
        for role, (email, first_name, last_name) in roles.items():
            user, created = RevelUser.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "language": "es",
                    "email_verified": True,
                    "is_staff": role == "admin",
                    "is_superuser": role == "admin",
                },
            )
            if created:
                user.set_password(credentials[role]["password"])
                user.save(update_fields=["password"])
            elif not user.check_password(credentials[role]["password"]):
                raise RuntimeError(
                    f"La credencial local no coincide con {email}; no se sobrescribió su contraseña."
                )
            users[role] = user

        city, _ = City.objects.get_or_create(
            city_id=3868707,
            defaults={
                "name": "Valdivia",
                "ascii_name": "Valdivia",
                "country": "Chile",
                "iso2": "CL",
                "iso3": "CHL",
                "admin_name": "Los Ríos",
                "capital": "admin",
                "population": 166080,
                "timezone": "America/Santiago",
                "location": Point(-73.2459, -39.8142, srid=4326),
            },
        )
        manifest: dict[str, t.Any] = {"organizations": {}, "events": {}, "tiers": {}}
        now = timezone.now()
        for suffix, name, title, event_id, org_id in [
            (
                "a",
                "Caudal Creativo · Demo",
                "Caudal en vivo · Sesión de prueba",
                "cafd0000-0000-4000-8000-000000000001",
                "cafd0000-0000-4000-8000-000000000101",
            ),
            (
                "b",
                "Colectivo Independiente · Demo",
                "Laboratorio creativo · Productor B",
                "cafd0000-0000-4000-8000-000000000002",
                "cafd0000-0000-4000-8000-000000000102",
            ),
        ]:
            organization, _ = Organization.objects.get_or_create(
                id=UUID(org_id),
                defaults={
                    "name": name,
                    "slug": f"caudal-demo-{suffix}",
                    "owner": users[f"producer_{suffix}"],
                    "visibility": Organization.Visibility.PUBLIC,
                    "description": "Productora de demostración para la primera prueba funcional de CaudalTickets.",
                    "city": city,
                    "vat_country_code": "CL",
                },
            )
            event, _ = Event.objects.get_or_create(
                id=UUID(event_id),
                defaults={
                    "organization": organization,
                    "name": title,
                    "slug": f"caudal-primera-prueba-{suffix}",
                    "description": (
                        "Encuentro de demostración de CaudalTickets: música, artes y colaboración creativa. "
                        "Permite probar reservas y validación QR. No se realizan cobros online."
                    ),
                    "visibility": Event.Visibility.PUBLIC,
                    "event_type": Event.EventType.PUBLIC,
                    "status": Event.EventStatus.OPEN,
                    "start": now + timedelta(days=14),
                    "end": now + timedelta(days=14, hours=4),
                    "check_in_starts_at": now - timedelta(hours=1),
                    "check_in_ends_at": now + timedelta(days=14, hours=4),
                    "requires_ticket": True,
                    "max_attendees": 0,
                    "max_tickets_per_user": None,
                    "city": city,
                    "address": "Espacio de demostración · Valdivia, Chile",
                },
            )
            # Relocate only the two explicit local fixtures, preserving purchases and IDs.
            if organization.city_id != city.id:
                organization.city = city
                organization.save(update_fields=["city"])
            if event.city_id != city.id:
                event.city = city
                event.address = "Espacio de demostración · Valdivia, Chile"
                event.save(update_fields=["city", "address"])
            # Configure Revel's auto-created default tier rather than leaving a stray 0-price offline tier.
            tier = event.ticket_tiers.filter(name="Entrada demo gratuita").first()
            if tier is None:
                tier = event.ticket_tiers.get(name=DEFAULT_TICKET_TIER_NAME)
                tier.name = "Entrada demo gratuita"
                tier.payment_method = TicketTier.PaymentMethod.FREE
                tier.currency = "EUR"
                tier.description = (
                    "Entrada sin costo para probar emisión de PDF y control de acceso."
                )
                tier.save()
            door_tier, _ = TicketTier.objects.get_or_create(
                event=event,
                name="Reserva demo · Pago en puerta",
                defaults={
                    "payment_method": TicketTier.PaymentMethod.AT_THE_DOOR,
                    "price": 10,
                    "currency": "EUR",
                    "description": "Reserva de prueba de 10 EUR. No cobra tarjeta ni confirma pago bancario.",
                    "display_order": 1,
                },
            )
            manifest["organizations"][suffix] = {
                "id": str(organization.id),
                "slug": organization.slug,
            }
            manifest["events"][suffix] = {
                "id": str(event.id),
                "slug": event.slug,
                "name": event.name,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
            }
            manifest["tiers"][suffix] = {
                "free": str(tier.id),
                "at_the_door": str(door_tier.id),
            }

    write_private_json(MANIFEST_PATH, manifest)
    return manifest


if __name__ == "__main__":
    seed_demo()
    print("Demo lista: dos productoras, dos eventos, comprador y administrador.")
    print("Credenciales locales: .local/demo-credentials.json (no subir a GitHub).")
    print("IDs y rutas de eventos: .local/demo.json.")
