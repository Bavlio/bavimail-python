"""Outbound email data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class AttachmentMetadata:
    """Metadata for an email attachment (no content)."""

    filename: str
    size_bytes: int
    mime_type: str
    content_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AttachmentMetadata:
        return cls(
            filename=data["filename"],
            size_bytes=data["size_bytes"],
            mime_type=data["mime_type"],
            content_id=data.get("content_id"),
        )


@dataclass(frozen=True)
class Email:
    """An outbound email sent via Bavimail.

    Attributes:
        id: Unique identifier for the email.
        alias_id: ID of the alias used to send the email.
        domain_id: ID of the domain the alias belongs to.
        from_email: Full sender email address.
        to_email: Recipient email address.
        subject: Email subject line.
        body_text: Plain text email body.
        status: Delivery status: "queued", "sending", "sent", "delivered", or "failed".
        provider_message_id: Message ID assigned by the email provider.
        user_id: ID of the user who sent this email.
        created_at: When the email was created.
        updated_at: When the email was last updated.
        conversation_id: ID of the conversation this email belongs to.
        body_html: HTML email body.
        in_reply_to: Message-ID of the email being replied to.
        references: RFC 5322 References header for threading.
        attachments: List of attachment metadata.
        attachment_count: Number of attachments.
        provider_metadata: Provider-specific metadata.
        sent_at: When the email was sent to the provider.
        delivered_at: When delivery was confirmed.
        error_message: Error message if sending failed.
        tracking_id: ID for open tracking pixel.
        track_opens: Whether open tracking is enabled.
        first_opened_at: When the email was first opened.
        open_count: Number of times the email was opened.
        alias_name: Name portion of the alias (e.g., "support").
        domain_name: Domain name (e.g., "example.com").
    """

    id: str
    alias_id: str
    domain_id: str
    from_email: str
    to_email: str
    subject: str
    body_text: str
    status: str
    provider_message_id: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    conversation_id: str | None = None
    body_html: str | None = None
    in_reply_to: str | None = None
    references: str | None = None
    attachments: list[AttachmentMetadata] | None = None
    attachment_count: int = 0
    provider_metadata: dict[str, Any] | None = field(default=None)
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    error_message: str | None = None
    tracking_id: str | None = None
    track_opens: bool = True
    first_opened_at: datetime | None = None
    open_count: int = 0
    alias_name: str | None = None
    domain_name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Email:
        attachments_raw = data.get("attachments")
        attachments = (
            [AttachmentMetadata.from_dict(a) for a in attachments_raw]
            if attachments_raw
            else None
        )
        return cls(
            id=str(data["id"]),
            alias_id=str(data["alias_id"]),
            domain_id=str(data["domain_id"]),
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            body_text=data["body_text"],
            status=data["status"],
            provider_message_id=data.get("provider_message_id", ""),
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            conversation_id=(
                str(data["conversation_id"]) if data.get("conversation_id") else None
            ),
            body_html=data.get("body_html"),
            in_reply_to=data.get("in_reply_to"),
            references=data.get("references"),
            attachments=attachments,
            attachment_count=data.get("attachment_count", 0),
            provider_metadata=data.get("provider_metadata"),
            sent_at=_parse_datetime(data.get("sent_at")),
            delivered_at=_parse_datetime(data.get("delivered_at")),
            error_message=data.get("error_message"),
            tracking_id=str(data["tracking_id"]) if data.get("tracking_id") else None,
            track_opens=data.get("track_opens", True),
            first_opened_at=_parse_datetime(data.get("first_opened_at")),
            open_count=data.get("open_count", 0),
            alias_name=data.get("alias_name"),
            domain_name=data.get("domain_name"),
        )
