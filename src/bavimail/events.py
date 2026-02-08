"""Event types, webhook event model, and event-specific data models."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from .models._base import _parse_datetime, _parse_datetime_required


class EventType(str, enum.Enum):
    """Bavimail webhook event types.

    Inherits ``str`` for Python 3.9 compatibility (``StrEnum`` is 3.11+).
    Values can be compared directly with strings and passed to
    ``webhooks.create(url, event_types)``.
    """

    OUTBOUND_SENT = "email.outbound.sent"
    OUTBOUND_FAILED = "email.outbound.failed"
    OUTBOUND_OPENED = "email.outbound.opened"
    OUTBOUND_CLICKED = "email.outbound.clicked"
    OUTBOUND_SCHEDULED = "email.outbound.scheduled"
    OUTBOUND_CANCELLED = "email.outbound.cancelled"
    OUTBOUND_DELIVERED = "email.outbound.delivered"
    OUTBOUND_BOUNCED = "email.outbound.bounced"
    OUTBOUND_COMPLAINED = "email.outbound.complained"
    INBOUND_RECEIVED = "email.inbound.received"
    DOMAIN_VERIFIED = "domain.verified"
    DOMAIN_FAILED = "domain.failed"
    WEBHOOK_TEST = "webhook.test"


@dataclass(frozen=True)
class WebhookEvent:
    """Parsed webhook delivery envelope.

    This is the object every event handler receives.

    Attributes:
        event_id: Unique identifier for this delivery.
        event_type: The event type as an :class:`EventType` member.
        timestamp: When the event was produced.
        data: Raw event payload dict.
    """

    event_id: str
    event_type: EventType
    timestamp: datetime
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> WebhookEvent:
        """Parse a raw webhook JSON dict into a :class:`WebhookEvent`.

        Raises:
            ValueError: If ``event_type`` is not a recognised :class:`EventType`.
        """
        return cls(
            event_id=raw["event_id"],
            event_type=EventType(raw["event_type"]),
            timestamp=_parse_datetime_required(raw["timestamp"]),
            data=raw.get("data", {}),
        )


# ---------------------------------------------------------------------------
# Event-specific data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InboundReceivedData:
    """Typed payload for ``email.inbound.received`` events."""

    email_id: str
    alias_id: str
    domain_id: str
    from_email: str
    to_email: str
    subject: str
    attachment_count: int
    has_html: bool
    from_name: Optional[str] = None
    body_preview: Optional[str] = None
    received_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InboundReceivedData:
        return cls(
            email_id=data["email_id"],
            alias_id=data["alias_id"],
            domain_id=data["domain_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            attachment_count=data["attachment_count"],
            has_html=data["has_html"],
            from_name=data.get("from_name"),
            body_preview=data.get("body_preview"),
            received_at=_parse_datetime(data.get("received_at")),
        )


@dataclass(frozen=True)
class OutboundSentData:
    """Typed payload for ``email.outbound.sent`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    body_preview: Optional[str] = None
    sent_at: Optional[datetime] = None
    provider_message_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundSentData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            body_preview=data.get("body_preview"),
            sent_at=_parse_datetime(data.get("sent_at")),
            provider_message_id=data.get("provider_message_id"),
        )


@dataclass(frozen=True)
class OutboundFailedData:
    """Typed payload for ``email.outbound.failed`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    error_message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundFailedData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            error_message=data.get("error_message"),
        )


@dataclass(frozen=True)
class OutboundOpenedData:
    """Typed payload for ``email.outbound.opened`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    is_first_open: bool
    is_bot: bool
    open_count: int
    opened_at: Optional[datetime] = None
    bot_reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundOpenedData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            is_first_open=data["is_first_open"],
            is_bot=data["is_bot"],
            open_count=data["open_count"],
            opened_at=_parse_datetime(data.get("opened_at")),
            bot_reason=data.get("bot_reason"),
        )


@dataclass(frozen=True)
class OutboundClickedData:
    """Typed payload for ``email.outbound.clicked`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    link_id: str
    original_url: str
    position: int
    is_first_click: bool
    is_bot: bool
    link_click_count: int
    link_unique_click_count: int
    email_click_count: int
    anchor_text: Optional[str] = None
    clicked_at: Optional[datetime] = None
    bot_reason: Optional[str] = None
    device_type: Optional[str] = None
    browser_name: Optional[str] = None
    os_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundClickedData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            link_id=data["link_id"],
            original_url=data["original_url"],
            position=data["position"],
            is_first_click=data["is_first_click"],
            is_bot=data["is_bot"],
            link_click_count=data["link_click_count"],
            link_unique_click_count=data["link_unique_click_count"],
            email_click_count=data["email_click_count"],
            anchor_text=data.get("anchor_text"),
            clicked_at=_parse_datetime(data.get("clicked_at")),
            bot_reason=data.get("bot_reason"),
            device_type=data.get("device_type"),
            browser_name=data.get("browser_name"),
            os_name=data.get("os_name"),
        )


@dataclass(frozen=True)
class OutboundScheduledData:
    """Typed payload for ``email.outbound.scheduled`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    send_at: Optional[datetime] = None
    send_at_timezone: Optional[str] = None
    send_at_utc: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundScheduledData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            send_at=_parse_datetime(data.get("send_at")),
            send_at_timezone=data.get("send_at_timezone"),
            send_at_utc=_parse_datetime(data.get("send_at_utc")),
        )


@dataclass(frozen=True)
class OutboundCancelledData:
    """Typed payload for ``email.outbound.cancelled`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    cancelled_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundCancelledData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            cancelled_at=_parse_datetime(data.get("cancelled_at")),
        )


@dataclass(frozen=True)
class DomainVerifiedData:
    """Typed payload for ``domain.verified`` events."""

    domain_id: str
    domain: str
    verified_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainVerifiedData:
        return cls(
            domain_id=data["domain_id"],
            domain=data["domain"],
            verified_at=_parse_datetime(data.get("verified_at")),
        )


@dataclass(frozen=True)
class DomainFailedData:
    """Typed payload for ``domain.failed`` events."""

    domain_id: str
    domain: str
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainFailedData:
        return cls(
            domain_id=data["domain_id"],
            domain=data["domain"],
            error=data.get("error"),
        )


@dataclass(frozen=True)
class WebhookTestData:
    """Typed payload for ``webhook.test`` events."""

    webhook_id: str
    test: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WebhookTestData:
        return cls(
            webhook_id=data["webhook_id"],
            test=data["test"],
        )


@dataclass(frozen=True)
class OutboundDeliveredData:
    """Typed payload for ``email.outbound.delivered`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    delivered_at: Optional[datetime] = None
    provider_message_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundDeliveredData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            delivered_at=_parse_datetime(data.get("delivered_at")),
            provider_message_id=data.get("provider_message_id"),
        )


@dataclass(frozen=True)
class OutboundBouncedData:
    """Typed payload for ``email.outbound.bounced`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    bounced_at: Optional[datetime] = None
    bounce_type: Optional[str] = None
    bounce_sub_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundBouncedData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            bounced_at=_parse_datetime(data.get("bounced_at")),
            bounce_type=data.get("bounce_type"),
            bounce_sub_type=data.get("bounce_sub_type"),
        )


@dataclass(frozen=True)
class OutboundComplainedData:
    """Typed payload for ``email.outbound.complained`` events."""

    email_id: str
    from_email: str
    to_email: str
    subject: str
    complained_at: Optional[datetime] = None
    complaint_feedback_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutboundComplainedData:
        return cls(
            email_id=data["email_id"],
            from_email=data["from_email"],
            to_email=data["to_email"],
            subject=data["subject"],
            complained_at=_parse_datetime(data.get("complained_at")),
            complaint_feedback_type=data.get("complaint_feedback_type"),
        )
