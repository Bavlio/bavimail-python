"""Tag data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class TagSummary:
    """Minimal tag info for embedding in other responses."""

    id: str
    name: str
    type: str
    color: str | None = None
    icon: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TagSummary:
        return cls(
            id=str(data["id"]),
            name=data["name"],
            type=data["type"],
            color=data.get("color"),
            icon=data.get("icon"),
        )


@dataclass(frozen=True)
class Tag:
    """A tag for organizing emails.

    Attributes:
        id: Unique identifier for the tag.
        name: Display name of the tag.
        type: Tag type: "tag" for user tags, "folder" for folder-like organization.
        sort_order: Position for ordering tags in the UI.
        is_pinned: Whether the tag is pinned to the top of the list.
        is_system: Whether this is a system-managed tag (e.g., "Inbox", "Sent").
        email_count: Number of emails with this tag.
        is_visible: Whether the tag is shown in the UI.
        user_id: ID of the user who owns this tag.
        created_at: When the tag was created.
        updated_at: When the tag was last updated.
        description: Optional description of the tag.
        color: Hex color code for the tag (e.g., "#ff0000").
        icon: Icon identifier for the tag.
    """

    id: str
    name: str
    type: str
    sort_order: int
    is_pinned: bool
    is_system: bool
    email_count: int
    is_visible: bool
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    description: str | None = None
    color: str | None = None
    icon: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Tag:
        return cls(
            id=str(data["id"]),
            name=data["name"],
            type=data["type"],
            sort_order=data.get("sort_order", 0),
            is_pinned=data.get("is_pinned", False),
            is_system=data.get("is_system", False),
            email_count=data.get("email_count", 0),
            is_visible=data.get("is_visible", True),
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            description=data.get("description"),
            color=data.get("color"),
            icon=data.get("icon"),
        )


@dataclass(frozen=True)
class EmailTag:
    """Tag applied to an email with metadata."""

    tag: TagSummary
    tagged_by: str
    tagged_at: datetime | None = None
    note: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailTag:
        return cls(
            tag=TagSummary.from_dict(data["tag"]),
            tagged_by=data["tagged_by"],
            tagged_at=_parse_datetime(data.get("tagged_at")),
            note=data.get("note"),
        )
