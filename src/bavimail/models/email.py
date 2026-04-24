"""Outbound email data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class AttachmentMetadata:
    """Metadata for an email attachment (no content)."""

    id: str | None = None
    filename: str | None = None
    size_bytes: int = 0
    mime_type: str = ""
    sha256: str | None = None
    content_id: str | None = None
    is_inline: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AttachmentMetadata:
        return cls(
            id=str(data["id"]) if data.get("id") else None,
            filename=data.get("filename"),
            size_bytes=data["size_bytes"],
            mime_type=data["mime_type"],
            sha256=data.get("sha256"),
            content_id=data.get("content_id"),
            is_inline=data.get("is_inline", False),
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
    to_emails: list[str]
    subject: str
    body_text: str
    status: str
    provider_message_id: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    conversation_id: str | None = None
    body_html: str | None = None
    cc_emails: list[str] | None = None
    bcc_emails: list[str] | None = None
    in_reply_to: str | None = None
    thread_references: str | None = None
    attachments: list[AttachmentMetadata] | None = None
    attachment_count: int = 0
    provider_metadata: dict[str, Any] | None = field(default=None)
    warmup_suspicious: bool = False
    warmup_suspicious_tokens: list[str] = field(default_factory=list)
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    error_message: str | None = None
    tracking_id: str | None = None
    track_opens: bool = True
    first_opened_at: datetime | None = None
    open_count: int = 0
    alias_name: str | None = None
    domain_name: str | None = None
    send_at: datetime | None = None
    send_at_timezone: str | None = None
    send_at_utc: datetime | None = None
    cancelled_at: datetime | None = None
    track_clicks: bool = False
    click_count: int = 0
    first_clicked_at: datetime | None = None
    last_clicked_at: datetime | None = None
    tracked_links_count: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Email:
        attachments_raw = data.get("attachments")
        warmup_tokens_raw = data.get("warmup_suspicious_tokens")
        attachments = (
            [AttachmentMetadata.from_dict(a) for a in attachments_raw] if attachments_raw else None
        )
        warmup_suspicious_tokens = (
            [str(token) for token in warmup_tokens_raw]
            if isinstance(warmup_tokens_raw, list)
            else []
        )
        return cls(
            id=str(data["id"]),
            alias_id=str(data["alias_id"]),
            domain_id=str(data["domain_id"]),
            from_email=data["from_email"],
            to_email=data["to_email"],
            to_emails=[str(email) for email in data.get("to_emails", [])],
            subject=data["subject"],
            body_text=data["body_text"],
            status=data["status"],
            provider_message_id=data.get("provider_message_id", ""),
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            conversation_id=(str(data["conversation_id"]) if data.get("conversation_id") else None),
            body_html=data.get("body_html"),
            cc_emails=(
                [str(email) for email in data["cc_emails"]]
                if data.get("cc_emails")
                else None
            ),
            bcc_emails=(
                [str(email) for email in data["bcc_emails"]] if data.get("bcc_emails") else None
            ),
            in_reply_to=data.get("in_reply_to"),
            thread_references=data.get("thread_references"),
            attachments=attachments,
            attachment_count=data.get("attachment_count", 0),
            provider_metadata=data.get("provider_metadata"),
            warmup_suspicious=bool(data.get("warmup_suspicious", False)),
            warmup_suspicious_tokens=warmup_suspicious_tokens,
            sent_at=_parse_datetime(data.get("sent_at")),
            delivered_at=_parse_datetime(data.get("delivered_at")),
            error_message=data.get("error_message"),
            tracking_id=str(data["tracking_id"]) if data.get("tracking_id") else None,
            track_opens=data.get("track_opens", True),
            first_opened_at=_parse_datetime(data.get("first_opened_at")),
            open_count=data.get("open_count", 0),
            alias_name=data.get("alias_name"),
            domain_name=data.get("domain_name"),
            send_at=_parse_datetime(data.get("send_at")),
            send_at_timezone=data.get("send_at_timezone"),
            send_at_utc=_parse_datetime(data.get("send_at_utc")),
            cancelled_at=_parse_datetime(data.get("cancelled_at")),
            track_clicks=data.get("track_clicks", False),
            click_count=data.get("click_count", 0),
            first_clicked_at=_parse_datetime(data.get("first_clicked_at")),
            last_clicked_at=_parse_datetime(data.get("last_clicked_at")),
            tracked_links_count=data.get("tracked_links_count", 0),
        )


@dataclass(frozen=True)
class EmailClick:
    """A click event on a tracked link in an email."""

    id: str
    link_id: str
    original_url: str
    position: int
    clicked_at: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_agent: str | None = None
    ip_address: str | None = None
    referer: str | None = None
    device_type: str | None = None
    browser_name: str | None = None
    os_name: str | None = None
    is_first_click: bool = False
    is_bot: bool = False
    bot_reason: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailClick:
        return cls(
            id=str(data["id"]),
            link_id=str(data["link_id"]),
            original_url=data["original_url"],
            position=data["position"],
            clicked_at=_parse_datetime(data["clicked_at"]),  # type: ignore[arg-type]
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            user_agent=data.get("user_agent"),
            ip_address=data.get("ip_address"),
            referer=data.get("referer"),
            device_type=data.get("device_type"),
            browser_name=data.get("browser_name"),
            os_name=data.get("os_name"),
            is_first_click=data.get("is_first_click", False),
            is_bot=data.get("is_bot", False),
            bot_reason=data.get("bot_reason"),
        )


@dataclass(frozen=True)
class TrackedLink:
    """A tracked link in an email."""

    id: str
    link_id: str
    original_url: str
    position: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    anchor_text: str | None = None
    click_count: int = 0
    unique_click_count: int = 0
    first_clicked_at: datetime | None = None
    last_clicked_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TrackedLink:
        return cls(
            id=str(data["id"]),
            link_id=str(data["link_id"]),
            original_url=data["original_url"],
            position=data["position"],
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            anchor_text=data.get("anchor_text"),
            click_count=data.get("click_count", 0),
            unique_click_count=data.get("unique_click_count", 0),
            first_clicked_at=_parse_datetime(data.get("first_clicked_at")),
            last_clicked_at=_parse_datetime(data.get("last_clicked_at")),
        )


@dataclass(frozen=True)
class BatchEmailItemError:
    """Error details for a failed item in a batch send."""

    message: str
    code: str | None = None
    category: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatchEmailItemError:
        return cls(
            message=data["message"],
            code=data.get("code"),
            category=data.get("category"),
        )


@dataclass(frozen=True)
class BatchEmailItemResult:
    """Result for a single item in a batch send."""

    index: int
    status: str
    email: Email | None = None
    error: BatchEmailItemError | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatchEmailItemResult:
        email_data = data.get("email")
        error_data = data.get("error")
        return cls(
            index=data["index"],
            status=data["status"],
            email=Email.from_dict(email_data) if email_data else None,
            error=BatchEmailItemError.from_dict(error_data) if error_data else None,
        )


@dataclass(frozen=True)
class BatchEmailResponse:
    """Response from a batch email send."""

    total: int
    accepted: int
    rejected: int
    results: list[BatchEmailItemResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatchEmailResponse:
        return cls(
            total=data["total"],
            accepted=data["accepted"],
            rejected=data["rejected"],
            results=[BatchEmailItemResult.from_dict(r) for r in data.get("results", [])],
        )


@dataclass(frozen=True)
class EmailEvent:
    """An event on an outbound email (delivery, bounce, complaint, etc.)."""

    id: str
    event_type: str
    occurred_at: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
    bounce_type: str | None = None
    bounce_sub_type: str | None = None
    complaint_feedback_type: str | None = None
    error_message: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailEvent:
        return cls(
            id=str(data["id"]),
            event_type=data["event_type"],
            occurred_at=_parse_datetime(data["occurred_at"]),  # type: ignore[arg-type]
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            bounce_type=data.get("bounce_type"),
            bounce_sub_type=data.get("bounce_sub_type"),
            complaint_feedback_type=data.get("complaint_feedback_type"),
            error_message=data.get("error_message"),
        )


@dataclass(frozen=True)
class EmailEventsResponse:
    """Paginated response for email events."""

    events: list[EmailEvent]
    total: int
    limit: int
    offset: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailEventsResponse:
        return cls(
            events=[EmailEvent.from_dict(e) for e in data.get("events", [])],
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
        )


@dataclass(frozen=True)
class EmailValidationCheck:
    """A single validation check result."""

    name: str
    passed: bool
    weight: float
    detail: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailValidationCheck:
        return cls(
            name=data["name"],
            passed=data["passed"],
            weight=data["weight"],
            detail=data["detail"],
        )


@dataclass(frozen=True)
class EmailValidationResponse:
    """Response from email validation endpoint."""

    email: str
    risk_score: float
    risk_level: str
    is_risky: bool
    checks: list[EmailValidationCheck] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EmailValidationResponse:
        return cls(
            email=data["email"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            is_risky=data["is_risky"],
            checks=[EmailValidationCheck.from_dict(c) for c in data.get("checks", [])],
        )
