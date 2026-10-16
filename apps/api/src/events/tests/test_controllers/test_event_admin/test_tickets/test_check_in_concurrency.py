"""Real-PostgreSQL regression for simultaneous door scans of the same QR."""

from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Event as ThreadEvent
from threading import Lock

import pytest
from django.db import close_old_connections, connection, connections, transaction
from django.utils import timezone, translation
from ninja.errors import HttpError
from pytest import MonkeyPatch

from accounts.models import RevelUser
from events.models import Event, Ticket, TicketTier
from events.service import check_in_service


@pytest.mark.django_db(transaction=True)
def test_simultaneous_scans_admit_exactly_once(
    event: Event,
    active_online_ticket: Ticket,
    organization_owner_user: RevelUser,
    monkeypatch: MonkeyPatch,
) -> None:
    """Separate committed connections model two scanners, unlike wrapped TestCase transactions.

    Pause the first scan after its real row read while the second scanner starts. Without
    serialization both see ACTIVE; with locking the second waits, then sees CHECKED_IN.
    The bounded wait also lets conditional-update solutions satisfy this behavior.
    """
    if connection.vendor != "postgresql":
        pytest.skip("This regression requires PostgreSQL row locking.")

    now = timezone.now()
    event.check_in_starts_at = now - timedelta(hours=1)
    event.check_in_ends_at = now + timedelta(hours=1)
    event.save(update_fields=["check_in_starts_at", "check_in_ends_at"])

    first_read = ThreadEvent()
    second_read = ThreadEvent()
    counter_lock = Lock()
    read_count = 0
    original_ensure_open = check_in_service._ensure_check_in_open

    def coordinate_scans(event: Event, tier: TicketTier) -> None:
        nonlocal read_count
        original_ensure_open(event, tier)
        with counter_lock:
            read_count += 1
            ordinal = read_count
        if ordinal == 1:
            first_read.set()
            second_read.wait(timeout=2)
        else:
            second_read.set()

    monkeypatch.setattr(check_in_service, "_ensure_check_in_open", coordinate_scans)

    def scan() -> tuple[int, str]:
        close_old_connections()
        try:
            # ATOMIC_REQUESTS wraps real HTTP scans in the same way.
            with transaction.atomic(), translation.override("en"):
                ticket = check_in_service.check_in_ticket(event, active_online_ticket.id, organization_owner_user)
                return 200, ticket.status
        except HttpError as error:
            return error.status_code, str(error.message)
        finally:
            connections.close_all()

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(scan)
        assert first_read.wait(timeout=5), "The first scanner never read the ticket."
        second = pool.submit(scan)
        results = [first.result(timeout=15), second.result(timeout=15)]

    assert sorted(status for status, _ in results) == [200, 400], results
    assert any("already been checked in" in detail for status, detail in results if status == 400)
    active_online_ticket.refresh_from_db()
    assert active_online_ticket.status == Ticket.TicketStatus.CHECKED_IN
    assert active_online_ticket.checked_in_by_id == organization_owner_user.id
