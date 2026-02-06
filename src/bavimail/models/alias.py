"""Alias data model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class Alias:
    """An email alias on a verified domain."""

    id: str
    domain_id: str
    alias: str
    full_email: str
    domain_name: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    signature_html: str | None = None
    signature_text: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Alias:
        return cls(
            id=str(data["id"]),
            domain_id=str(data["domain_id"]),
            alias=data["alias"],
            full_email=data["full_email"],
            domain_name=data["domain_name"],
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            signature_html=data.get("signature_html"),
            signature_text=data.get("signature_text"),
        )
