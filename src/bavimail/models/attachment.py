"""Stored attachment models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class AttachmentFile:
    """A stored attachment file."""

    id: str
    user_id: str
    filename: str
    size_bytes: int
    mime_type: str
    sha256: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AttachmentFile:
        return cls(
            id=str(data["id"]),
            user_id=str(data["user_id"]),
            filename=data["filename"],
            size_bytes=data["size_bytes"],
            mime_type=data["mime_type"],
            sha256=data["sha256"],
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
        )


@dataclass(frozen=True)
class AttachmentUploadFile:
    """Binary content to upload into attachment storage."""

    filename: str
    content: bytes
    mime_type: str | None = None


@dataclass(frozen=True)
class AttachmentUploadResponse:
    """Response from uploading one or more attachments."""

    attachments: list[AttachmentFile]
    uploaded_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AttachmentUploadResponse:
        attachments = [AttachmentFile.from_dict(item) for item in data.get("attachments", [])]
        return cls(
            attachments=attachments,
            uploaded_at=_parse_datetime(data.get("uploaded_at")),
        )
