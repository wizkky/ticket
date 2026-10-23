#!/usr/bin/env python3
"""Exercise the running API's checkout, PDF/QR, access control and duplicate scan.

Creates three real demo reservations per run; does not delete or reset previous orders.
Requires seed_demo.py, pdftoppm (poppler-utils), pyzbar, and the zbar system library.
Run: scripts/smoke.sh [--base-url http://127.0.0.1:8000]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from decimal import Decimal
import sys
import typing as t
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from threading import Barrier
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")
    require(
        urlparse(base_url).hostname in {"localhost", "127.0.0.1", "::1"},
        "Usa esta prueba con una API local demo.",
    )
    for command in ("pdftoppm",):
        require(
            shutil.which(command) is not None, f"Falta {command}; ejecutar setup.sh."
        )
    from PIL import Image
    from pyzbar.pyzbar import decode

    credentials = json.loads((LOCAL / "demo-credentials.json").read_text())
    demo = json.loads((LOCAL / "demo.json").read_text())
    results: list[str] = []

    def request(
        method: str,
        path: str,
        *,
        token: str | None = None,
        body: dict[str, t.Any] | None = None,
        expected: tuple[int, ...] = (200,),
        binary: bool = False,
    ) -> t.Any:
        headers = {
            "Accept": "application/pdf" if binary else "application/json",
            "Accept-Language": "en",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode()
        req = Request(
            urljoin(base_url + "/", path), data=data, headers=headers, method=method
        )
        try:
            with urlopen(req, timeout=60) as response:
                status, content = response.status, response.read()
        except HTTPError as error:
            status, content = error.code, error.read()
        # Do not print response bodies: auth endpoints return credentials/tokens.
        require(
            status in expected,
            f"{method} {urlparse(path).path}: HTTP {status}; se esperaba {expected}.",
        )
        if binary:
            return content
        if not content:
            return None
        return json.loads(content)

    def passed(message: str) -> None:
        results.append(message)
        print(f"OK · {message}")

    tokens = {}
    request(
        "POST",
        "/api/auth/token/pair",
        body={
            "username": credentials["buyer"]["email"],
            "password": "intentionally-wrong-demo-password",
        },
        expected=(401,),
    )
    for role in ("producer_a", "producer_b", "buyer"):
        account = credentials[role]
        auth = request(
            "POST",
            "/api/auth/token/pair",
            body={"username": account["email"], "password": account["password"]},
        )
        require(bool(auth.get("access")), f"No se obtuvo sesión para {role}.")
        tokens[role] = auth["access"]
    passed("Ingreso real con contraseña: comprador y dos productores")

    event_a, event_b = demo["events"]["a"]["id"], demo["events"]["b"]["id"]
    org_a, org_b = (
        demo["organizations"]["a"]["slug"],
        demo["organizations"]["b"]["slug"],
    )
    for event_id in (event_a, event_b):
        tiers = request("GET", f"/api/events/{event_id}/tickets/tiers")
        require(len(tiers) >= 2, "El evento público no ofrece sus dos tarifas demo.")
    passed("Eventos y tarifas visibles sin iniciar sesión")

    for role, own_org, other_org, own_event, other_event in (
        ("producer_a", org_a, org_b, event_a, event_b),
        ("producer_b", org_b, org_a, event_b, event_a),
    ):
        token = tokens[role]
        request("GET", f"/api/organization-admin/{own_org}", token=token)
        request(
            "GET",
            f"/api/organization-admin/{other_org}",
            token=token,
            expected=(403, 404),
        )
        request("GET", f"/api/event-admin/{own_event}/tickets", token=token)
        request(
            "GET",
            f"/api/event-admin/{other_event}/tickets",
            token=token,
            expected=(403, 404),
        )
    passed("Ambos productores administran sus datos y no los del otro")

    door_tier_path = (
        f"/api/event-admin/{event_a}/ticket-tier/{demo['tiers']['a']['at_the_door']}"
    )
    tier_update = {"currency": demo["tiers"]["a"]["currency"], "price": demo["tiers"]["a"]["price"]}
    request(
        "PUT",
        door_tier_path,
        token=tokens["producer_b"],
        body=tier_update,
        expected=(403, 404),
    )
    request("PUT", door_tier_path, token=tokens["producer_a"], body=tier_update)
    passed(
        "Tarifa CLP editable vía API por su productor; otro productor no puede modificarla"
    )

    checkout_path = f"/api/events/{event_a}/checkout"
    payload = {
        "items": [
            {
                "tier_id": demo["tiers"]["a"]["free"],
                "tickets": [{"guest_name": "Compradora Demo Caudal"}],
            }
        ]
    }
    request("POST", checkout_path, body=payload, expected=(401,))
    checkout = request("POST", checkout_path, token=tokens["buyer"], body=payload)
    require(
        checkout.get("requires_payment") is False,
        "La tarifa gratis no completó el checkout.",
    )
    require(
        len(checkout.get("tickets", [])) == 1,
        "El checkout no emitió exactamente una entrada.",
    )
    ticket = checkout["tickets"][0]
    ticket_id = str(UUID(ticket["id"]))
    require(ticket["status"] == "active", "La entrada gratuita no está activa.")
    passed("Checkout real emite una entrada gratuita activa")

    pdf_path = f"/api/tickets/{ticket_id}/pdf"
    request("GET", pdf_path, expected=(401,))
    request("GET", pdf_path, token=tokens["producer_b"], expected=(404,))
    pdf = request("GET", pdf_path, token=tokens["buyer"], binary=True)
    require(
        pdf.startswith(b"%PDF-") and len(pdf) > 1000,
        "El archivo de entrada no es un PDF válido.",
    )
    output = LOCAL / "smoke"
    output.mkdir(parents=True, exist_ok=True)
    pdf_file = output / "entrada-gratuita.pdf"
    pdf_file.write_bytes(pdf)
    image_prefix = output / "entrada-gratuita"
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "1",
            "-singlefile",
            "-r",
            "180",
            "-png",
            str(pdf_file),
            str(image_prefix),
        ],
        capture_output=True,
        check=True,
        timeout=60,
    )
    with Image.open(image_prefix.with_suffix(".png")) as image:
        decoded = [code.data.decode() for code in decode(image)]
    require(
        decoded == [ticket_id], "El QR del PDF no coincide con la entrada comprada."
    )
    passed("PDF descargado por su dueño y QR leído desde la imagen real")

    check_in_path = f"/api/event-admin/{event_a}/tickets/{decoded[0]}/check-in"
    request("POST", check_in_path, token=tokens["buyer"], body={}, expected=(403,))
    request(
        "POST", check_in_path, token=tokens["producer_b"], body={}, expected=(403, 404)
    )
    checked_in = request("POST", check_in_path, token=tokens["producer_a"], body={})
    require(
        checked_in.get("status") == "checked_in",
        "El primer escaneo no registró acceso.",
    )
    duplicate = request(
        "POST", check_in_path, token=tokens["producer_a"], body={}, expected=(400,)
    )
    require(
        duplicate.get("detail")
        in {
            "This ticket has already been checked in.",
            "Esta entrada ya ha pasado el check-in.",
        },
        "El segundo escaneo falló por una razón distinta a duplicado.",
    )
    passed("Primer escaneo admite; segundo escaneo secuencial rechaza duplicado")

    concurrent_checkout = request(
        "POST", checkout_path, token=tokens["buyer"], body=payload
    )
    concurrent_id = concurrent_checkout["tickets"][0]["id"]
    concurrent_path = f"/api/event-admin/{event_a}/tickets/{concurrent_id}/check-in"
    start_scans = Barrier(2)

    def simultaneous_scan() -> int:
        start_scans.wait(timeout=10)
        response = request(
            "POST",
            concurrent_path,
            token=tokens["producer_a"],
            body={},
            expected=(200, 400),
        )
        if response.get("status") == "checked_in":
            return 200
        require(
            response.get("detail")
            in {
                "This ticket has already been checked in.",
                "Esta entrada ya ha pasado el check-in.",
            },
            "El escaneo concurrente falló por una razón distinta a duplicado.",
        )
        return 400

    with ThreadPoolExecutor(max_workers=2) as pool:
        scans = [pool.submit(simultaneous_scan) for _ in range(2)]
        scan_statuses = sorted(scan.result(timeout=65) for scan in scans)
    require(
        scan_statuses == [200, 400],
        "Dos escaneos simultáneos admitieron la misma entrada.",
    )
    passed("Dos peticiones HTTP simultáneas admiten exactamente una vez el mismo QR")

    paid_payload = {
        "items": [
            {
                "tier_id": demo["tiers"]["a"]["at_the_door"],
                "tickets": [{"guest_name": "Reserva Pago en Puerta"}],
            }
        ]
    }
    door = request("POST", checkout_path, token=tokens["buyer"], body=paid_payload)
    require(
        door.get("requires_payment") is False and len(door.get("tickets", [])) == 1,
        "No se completó la reserva con pago en puerta.",
    )
    door_ticket = door["tickets"][0]
    require(
        door_ticket["tier"]["payment_method"] == "at_the_door",
        "La reserva usa otro medio de pago.",
    )
    require(
        door_ticket["tier"]["currency"] == demo["tiers"]["a"]["currency"]
        and Decimal(str(door_ticket["tier"]["price"])) == Decimal(demo["tiers"]["a"]["price"]),
        "La reserva no respeta el precio configurado en pesos chilenos.",
    )
    require(
        door_ticket["payment"] is None,
        "La reserva en puerta creó un pago online inesperado.",
    )
    passed("Reserva en CLP con pago en puerta sin simular pago de tarjeta")

    buyer_tickets = request("GET", "/api/dashboard/tickets", token=tokens["buyer"])
    ids = {item["id"] for item in buyer_tickets["results"]}
    require(
        {ticket_id, door_ticket["id"]} <= ids,
        "Las entradas no aparecen en la cuenta del comprador.",
    )
    passed("Entradas visibles en la cuenta del comprador")

    from email_check import verify_ticket_email

    verify_ticket_email(
        ticket_id, credentials["buyer"]["email"], demo["events"]["a"]["name"]
    )
    passed("Correo real de la compra capturado en Mailpit con PDF e invitación ICS")

    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "passed": results,
        "ticket_id": ticket_id,
        "concurrent_ticket_id": concurrent_id,
        "door_ticket_id": door_ticket["id"],
        "online_payment": "pending: requiere credenciales sandbox y webhook de una pasarela compatible",
        "limits": [
            "Concurrencia HTTP comprobada y regresión PostgreSQL disponible por separado.",
            "Entorno de desarrollo, no producción.",
        ],
    }
    (output / "resultado.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        "Resultado guardado en .local/smoke/resultado.json. Pago online pendiente de sandbox."
    )


if __name__ == "__main__":
    try:
        main()
    except (
        RuntimeError,
        OSError,
        ValueError,
        KeyError,
        URLError,
        subprocess.SubprocessError,
    ) as error:
        # Never echo subprocess stdout or credential-bearing HTTP response bodies.
        print(f"ERROR · {error}", file=sys.stderr)
        sys.exit(1)
