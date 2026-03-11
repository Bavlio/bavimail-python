"""Inbound email data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class Verdict:
    """SES verdict result for spam, virus, SPF, DKIM, or DMARC."""

    status: str
    details: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Verdict | None:
        if data is None:
            return None
        return cls(status=data["status"], details=data.get("details"))


@dataclass(frozen=True)
class TagSummaryEmbed:
    """Minimal tag info embedded in email responses."""

    id: str
    name: str
    type: str
    color: str | None = None
    icon: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TagSummaryEmbed:
        return cls(
            id=str(data["id"]),
            name=data["name"],
            type=data["type"],
            color=data.get("color"),
            icon=data.get("icon"),
        )


@dataclass(frozen=True)
class InboundAttachmentMetadata:
    """Attachment metadata from an inbound email."""

    id: str | None = None
    size_bytes: int
    mime_type: str
    is_inline: bool
    filename: str | None = None
    sha256: str | None = None
    content_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InboundAttachmentMetadata:
        return cls(
            id=str(data["id"]) if data.get("id") else None,
            size_bytes=data["size_bytes"],
            mime_type=data["mime_type"],
            is_inline=data["is_inline"],
            filename=data.get("filename"),
            sha256=data.get("sha256"),
            content_id=data.get("content_id"),
        )


@dataclass(frozen=True)
class InboundEmailSummary:
    """Summary view of an inbound email for list operations.

    Attributes:
        id: Unique identifier for the inbound email.
        alias_id: ID of the alias that received the email.
        domain_id: ID of the domain the alias belongs to.
        from_email: Sender's email address.
        subject: Email subject line.
        alias_name: Name portion of the receiving alias (e.g., "support").
        domain_name: Domain name (e.g., "example.com").
        full_email: Full receiving email address (e.g., "support@example.com").
        attachment_count: Number of attachments.
        has_html: Whether the email has an HTML body.
        provider_message_id: Message ID assigned by the email provider.
        raw_email_uri: Storage URI for the raw RFC 822 email.
        user_id: ID of the user who owns this email.
        created_at: When the email record was created.
        updated_at: When the email was last updated.
        conversation_id: ID of the conversation this email belongs to.
        from_name: Display name of the sender.
        provider_received_at: When the provider received the email.
        processed_at: When the email was fully processed.
        processing_error: Error message if processing failed.
        provider_metadata: Provider-specific metadata.
        tags: Tags applied to this email.
    """

    id: str
    alias_id: str
    domain_id: str
    from_email: str
    subject: str
    alias_name: str
    domain_name: str
    full_email: str
    attachment_count: int
    has_html: bool
    provider_message_id: str
    raw_email_uri: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    conversation_id: str | None = None
    from_name: str | None = None
    provider_received_at: datetime | None = None
    processed_at: datetime | None = None
    processing_error: str | None = None
    provider_metadata: dict[str, Any] | None = field(default=None)
    tags: list[TagSummaryEmbed] | None = field(default=None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InboundEmailSummary:
        tags_raw = data.get("tags")
        tags = [TagSummaryEmbed.from_dict(t) for t in tags_raw] if tags_raw else None
        return cls(
            id=str(data["id"]),
            alias_id=str(data["alias_id"]),
            domain_id=str(data["domain_id"]),
            from_email=data["from_email"],
            subject=data["subject"],
            alias_name=data["alias_name"],
            domain_name=data["domain_name"],
            full_email=data["full_email"],
            attachment_count=data["attachment_count"],
            has_html=data["has_html"],
            provider_message_id=data["provider_message_id"],
            raw_email_uri=data["raw_email_uri"],
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            conversation_id=(str(data["conversation_id"]) if data.get("conversation_id") else None),
            from_name=data.get("from_name"),
            provider_received_at=_parse_datetime(data.get("provider_received_at")),
            processed_at=_parse_datetime(data.get("processed_at")),
            processing_error=data.get("processing_error"),
            provider_metadata=data.get("provider_metadata"),
            tags=tags,
        )


@dataclass(frozen=True)
class InboundEmailDetail:
    """Full detail view of an inbound email.

    Attributes:
        id: Unique identifier for the inbound email.
        alias_id: ID of the alias that received the email.
        domain_id: ID of the domain the alias belongs to.
        from_email: Sender's email address.
        to_email: Recipient email address.
        subject: Email subject line.
        alias_name: Name portion of the receiving alias (e.g., "support").
        domain_name: Domain name (e.g., "example.com").
        full_email: Full receiving email address (e.g., "support@example.com").
        attachment_count: Number of attachments.
        has_html: Whether the email has an HTML body.
        provider_message_id: Message ID assigned by the email provider.
        raw_email_uri: Storage URI for the raw RFC 822 email.
        user_id: ID of the user who owns this email.
        created_at: When the email record was created.
        updated_at: When the email was last updated.
        conversation_id: ID of the conversation this email belongs to.
        from_name: Display name of the sender.
        reply_to: Reply-To header address.
        cc_emails: List of CC recipient addresses.
        bcc_emails: List of BCC recipient addresses.
        body_text: Plain text email body.
        body_html: HTML email body.
        raw_email_size: Size of the raw email in bytes.
        headers: Parsed email headers.
        message_id: RFC 5322 Message-ID header.
        in_reply_to: Message-ID of the email being replied to.
        references: List of Message-IDs for threading.
        attachments: List of attachment metadata.
        provider_received_at: When the provider received the email.
        spam_verdict: Spam check result from email provider.
        virus_verdict: Virus scan result from email provider.
        spf_verdict: SPF authentication result.
        dkim_verdict: DKIM authentication result.
        dmarc_verdict: DMARC policy evaluation result.
        processed_at: When the email was fully processed.
        processing_error: Error message if processing failed.
        provider_metadata: Provider-specific metadata.
        tags: Tags applied to this email.
    """

    id: str
    alias_id: str
    domain_id: str
    from_email: str
    to_email: str
    subject: str
    alias_name: str
    domain_name: str
    full_email: str
    attachment_count: int
    has_html: bool
    provider_message_id: str
    raw_email_uri: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    conversation_id: str | None = None
    from_name: str | None = None
    reply_to: str | None = None
    cc_emails: list[str] | None = None
    bcc_emails: list[str] | None = None
    body_text: str | None = None
    body_html: str | None = None
    raw_email_size: int | None = None
    headers: dict[str, str] | None = None
    message_id: str | None = None
    in_reply_to: str | None = None
    thread_references: list[str] | None = None
    attachments: list[InboundAttachmentMetadata] | None = None
    provider_received_at: datetime | None = None
    spam_verdict: Verdict | None = None
    virus_verdict: Verdict | None = None
    spf_verdict: Verdict | None = None
    dkim_verdict: Verdict | None = None
    dmarc_verdict: Verdict | None = None
    processed_at: datetime | None = None
    processing_error: str | None = None
    provider_metadata: dict[str, Any] | None = field(default=None)
    tags: list[TagSummaryEmbed] | None = field(default=None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InboundEmailDetail:
        attachments_raw = data.get("attachments")
        attachments = (
            [InboundAttachmentMetadata.from_dict(a) for a in attachments_raw]
            if attachments_raw
            else None
        )
        tags_raw = data.get("tags")
        tags = [TagSummaryEmbed.from_dict(t) for t in tags_raw] if tags_raw else None
        return cls(
            id=str(data["id"]),
            alias_id=str(data["alias_id"]),
            domain_id=str(data["domain_id"]),
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            alias_name=data["alias_name"],
            domain_name=data["domain_name"],
            full_email=data["full_email"],
            attachment_count=data["attachment_count"],
            has_html=data["has_html"],
            provider_message_id=data["provider_message_id"],
            raw_email_uri=data["raw_email_uri"],
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            conversation_id=(str(data["conversation_id"]) if data.get("conversation_id") else None),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            cc_emails=data.get("cc_emails"),
            bcc_emails=data.get("bcc_emails"),
            body_text=data.get("body_text"),
            body_html=data.get("body_html"),
            raw_email_size=data.get("raw_email_size"),
            headers=data.get("headers"),
            message_id=data.get("message_id"),
            in_reply_to=data.get("in_reply_to"),
            thread_references=data.get("thread_references"),
            attachments=attachments,
            provider_received_at=_parse_datetime(data.get("provider_received_at")),
            spam_verdict=Verdict.from_dict(data.get("spam_verdict")),
            virus_verdict=Verdict.from_dict(data.get("virus_verdict")),
            spf_verdict=Verdict.from_dict(data.get("spf_verdict")),
            dkim_verdict=Verdict.from_dict(data.get("dkim_verdict")),
            dmarc_verdict=Verdict.from_dict(data.get("dmarc_verdict")),
            processed_at=_parse_datetime(data.get("processed_at")),
            processing_error=data.get("processing_error"),
            provider_metadata=data.get("provider_metadata"),
            tags=tags,
        )
