#!/usr/bin/env python3
"""Verify that an actual demo checkout delivered its PDF and calendar to Mailpit.

Run after scripts/smoke.sh, or call verify_ticket_email from the smoke workflow.
This checker reads local Mailpit only; it does not send a synthetic email or need
credentials, tokens, or an external SMTP provider.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from email import policy
from email.parser import BytesParser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote, urlparse
from urllib.request import urlopen
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"


def verify_ticket_email(
    ticket_id: str,
    buyer_email: str,
    event_name: str,
    mailpit_url: str = "http://127.0.0.1:8025",
) -> dict:
    """Find the buyer's checkout notification and validate its actual attachments.

    No email body or headers are printed or saved: those can contain signed
    unsubscribe URLs. The saved evidence includes only IDs and attachment sizes.
    """
    ticket_id = str(UUID(ticket_id))
    if urlparse(mailpit_url).hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise RuntimeError("La comprobación de correo requiere un Mailpit local.")
    mailpit_url = mailpit_url.rstrip("/")

    def get(path: str) -> bytes:
        with urlopen(mailpit_url + path, timeout=15) as response:
            return response.read()

    messages = json.loads(get("/api/v1/messages?limit=1000"))
    safe_buyer_suffix = "+" + buyer_email.lower().replace("@", "_at_").replace(
        ".", "_dot_"
    )

    def is_buyer_address(address: str) -> bool:
        address = address.lower()
        # Revel protects development installations by rewriting recipients to a
        # catchall address. Accept its lossless encoding of this buyer while
        # preserving the default live_emails=False setting.
        return address == buyer_email.lower() or address.split("@", 1)[0].endswith(
            safe_buyer_suffix
        )

    # Mailpit lists recent messages first. Inspect the envelope before retrieving
    # raw MIME so unrelated mail stays untouched.
    for summary in messages["messages"]:
        if not any(
            is_buyer_address(recipient.get("Address", ""))
            for recipient in summary.get("To", [])
        ):
            continue
        message_id = str(summary["ID"])
        message = BytesParser(policy=policy.default).parsebytes(
            get(f"/api/v1/message/{quote(message_id, safe='')}/raw")
        )
        text_parts = []
        attachments = {}
        for part in message.walk():
            filename = part.get_filename()
            if filename:
                attachments[filename] = (
                    part.get_content_type(),
                    part.get_payload(decode=True),
                )
            elif part.get_content_type() in {"text/plain", "text/html"}:
                text_parts.append(part.get_content())
        body = "\n".join(text_parts)
        if ticket_id not in body:
            continue
        if event_name not in body:
            raise RuntimeError("El correo de entrada no identifica el evento esperado.")
        pdf_type, pdf = attachments.get("ticket.pdf", ("", b""))
        if (
            pdf_type != "application/pdf"
            or not isinstance(pdf, bytes)
            or not pdf.startswith(b"%PDF-")
            or len(pdf) < 1000
        ):
            raise RuntimeError(
                "El correo de compra no contiene una entrada PDF válida."
            )
        calendar_type, calendar = attachments.get("event.ics", ("", b""))
        if (
            calendar_type != "text/calendar"
            or not isinstance(calendar, bytes)
            or b"BEGIN:VCALENDAR" not in calendar
        ):
            raise RuntimeError(
                "El correo de compra no contiene el calendario del evento."
            )

        output = LOCAL / "smoke"
        output.mkdir(parents=True, exist_ok=True, mode=0o700)
        pdf_path = output / "entrada-email.pdf"
        pdf_path.write_bytes(pdf)
        os.chmod(pdf_path, 0o600)
        report = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "ticket_id": ticket_id,
            "mailpit_message_id": message_id,
            "buyer_recipient_verified": True,
            "development_catchall": any(
                recipient.get("Address", "").lower() != buyer_email.lower()
                and is_buyer_address(recipient.get("Address", ""))
                for recipient in summary.get("To", [])
            ),
            "ticket_reference_verified": True,
            "event_name_verified": True,
            "attachments": {
                filename: {"type": content_type, "bytes": len(content)}
                for filename, (content_type, content) in attachments.items()
            },
        }
        report_path = output / "email-result.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        os.chmod(report_path, 0o600)
        return report
    raise RuntimeError(
        "Mailpit no recibió el correo de la entrada comprada en esta prueba."
    )


def main() -> None:
    smoke = json.loads((LOCAL / "smoke/resultado.json").read_text())
    credentials = json.loads((LOCAL / "demo-credentials.json").read_text())
    demo = json.loads((LOCAL / "demo.json").read_text())
    verify_ticket_email(
        smoke["ticket_id"],
        credentials["buyer"]["email"],
        demo["events"]["a"]["name"],
    )
    print(
        "OK · Correo de compra real recibido en Mailpit con entrada PDF y calendario ICS."
    )
    print("Evidencia local: .local/smoke/email-result.json y entrada-email.pdf.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, URLError) as error:
        # Never echo MIME contents or credential-bearing response bodies.
        print(f"ERROR · {error}", file=sys.stderr)
        sys.exit(1)
