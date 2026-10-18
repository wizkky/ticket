"""Small read models for the Caudal operational workspaces."""

import typing as t
from uuid import UUID

from ninja import Schema
from pydantic import AwareDatetime

from events.models import Event


class CaudalOrganization(Schema):
    id: UUID
    slug: str
    name: str
    role: t.Literal["owner", "staff"]


class CaudalWorkspace(Schema):
    platform_admin: bool
    organizations: list[CaudalOrganization]


class CaudalMetrics(Schema):
    issued: int
    door_reservations: int
    pending: int
    admissions: int
    online_payments: int


class CaudalEvent(Schema):
    organization_slug: str
    id: UUID
    name: str
    slug: str
    start: AwareDatetime
    status: Event.EventStatus
    city: str | None
    issued: int | None
    admissions: int | None


class CaudalProducerOverview(Schema):
    event_count: int
    metrics: CaudalMetrics | None
    events: list[CaudalEvent]


class CaudalAdminSection(Schema):
    key: str
    count: int
    path: str


class CaudalAdminOverview(Schema):
    metrics: CaudalMetrics
    sections: list[CaudalAdminSection]
    organizations: list[CaudalOrganization]
    producer_count: int
