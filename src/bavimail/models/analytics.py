"""Analytics data models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class DeliverabilitySummary:
    range: str
    total_sent: int
    delivered: int
    bounced: int
    complained: int
    opened: int
    clicked: int
    delivery_rate: float
    bounce_rate: float
    complaint_rate: float
    open_rate: float
    click_rate: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeliverabilitySummary:
        return cls(**data)


@dataclass(frozen=True)
class DeliverabilityTimeseriesPoint:
    bucket_start: object
    sent: int
    delivered: int
    bounced: int
    complained: int
    opened: int
    clicked: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeliverabilityTimeseriesPoint:
        return cls(
            bucket_start=_parse_datetime(data.get("bucket_start")),
            sent=data["sent"],
            delivered=data["delivered"],
            bounced=data["bounced"],
            complained=data["complained"],
            opened=data["opened"],
            clicked=data["clicked"],
        )


@dataclass(frozen=True)
class DeliverabilityTimeseries:
    range: str
    bucket: str
    points: list[DeliverabilityTimeseriesPoint]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeliverabilityTimeseries:
        return cls(
            range=data["range"],
            bucket=data["bucket"],
            points=[DeliverabilityTimeseriesPoint.from_dict(p) for p in data.get("points", [])],
        )


@dataclass(frozen=True)
class DeliverabilityRecentRow:
    email_id: str
    conversation_id: str | None
    subject: str
    recipient: str
    status: str
    sent_at: object
    delivered_at: object
    open_count: int
    click_count: int
    bounce_type: str | None
    complaint_feedback_type: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeliverabilityRecentRow:
        return cls(
            email_id=str(data["email_id"]),
            conversation_id=(str(data["conversation_id"]) if data.get("conversation_id") else None),
            subject=data["subject"],
            recipient=data["recipient"],
            status=data["status"],
            sent_at=_parse_datetime(data.get("sent_at")),
            delivered_at=_parse_datetime(data.get("delivered_at")),
            open_count=data["open_count"],
            click_count=data["click_count"],
            bounce_type=data.get("bounce_type"),
            complaint_feedback_type=data.get("complaint_feedback_type"),
        )


@dataclass(frozen=True)
class DeliverabilityRecent:
    rows: list[DeliverabilityRecentRow]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeliverabilityRecent:
        return cls(rows=[DeliverabilityRecentRow.from_dict(r) for r in data.get("rows", [])])
