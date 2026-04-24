"""Suppression data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class Suppression:
    id: str
    user_id: str
    email: str
    reason: str
    source: str
    status: str
    metadata: dict[str, Any]
    suppressed_at: datetime | None
    note: str | None = None
    released_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Suppression:
        return cls(
            id=str(data["id"]),
            user_id=str(data["user_id"]),
            email=data["email"],
            reason=data["reason"],
            source=data["source"],
            status=data["status"],
            note=data.get("note"),
            metadata=data.get("metadata", {}),
            suppressed_at=_parse_datetime(data.get("suppressed_at")),
            released_at=_parse_datetime(data.get("released_at")),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
        )
