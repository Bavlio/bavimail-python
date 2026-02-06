"""Conversation data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class ConversationSummary:
    """Summary view of a conversation for list operations."""

    id: str
    subject: str
    message_count: int
    user_id: str
    first_message_at: datetime | None = None
    last_message_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    first_from_email: str | None = None
    first_to_email: str | None = None
    total_attachment_count: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationSummary:
        return cls(
            id=str(data["id"]),
            subject=data["subject"],
            message_count=data["message_count"],
            user_id=str(data["user_id"]),
            first_message_at=_parse_datetime(data.get("first_message_at")),
            last_message_at=_parse_datetime(data.get("last_message_at")),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            first_from_email=data.get("first_from_email"),
            first_to_email=data.get("first_to_email"),
            total_attachment_count=data.get("total_attachment_count", 0),
        )


@dataclass(frozen=True)
class ConversationMessage:
    """A single message within a conversation thread."""

    id: str
    direction: str
    from_email: str
    to_email: str
    subject: str
    attachment_count: int
    timestamp: datetime | None = None
    from_name: str | None = None
    body_text: str | None = None
    body_html: str | None = None
    message_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationMessage:
        return cls(
            id=str(data["id"]),
            direction=data["direction"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            attachment_count=data["attachment_count"],
            timestamp=_parse_datetime(data.get("timestamp")),
            from_name=data.get("from_name"),
            body_text=data.get("body_text"),
            body_html=data.get("body_html"),
            message_id=data.get("message_id"),
        )


@dataclass(frozen=True)
class ConversationDetail:
    """Full conversation detail with all messages."""

    id: str
    subject: str
    message_count: int
    messages: list[ConversationMessage]
    user_id: str
    first_message_at: datetime | None = None
    last_message_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationDetail:
        return cls(
            id=str(data["id"]),
            subject=data["subject"],
            message_count=data["message_count"],
            messages=[
                ConversationMessage.from_dict(m) for m in data.get("messages", [])
            ],
            user_id=str(data["user_id"]),
            first_message_at=_parse_datetime(data.get("first_message_at")),
            last_message_at=_parse_datetime(data.get("last_message_at")),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
        )
