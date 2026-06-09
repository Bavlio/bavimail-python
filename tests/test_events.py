"""Tests for EventType, WebhookEvent, and event-specific data models."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from bavimail.events import (
    DomainFailedData,
    DomainVerifiedData,
    EventType,
    InboundReceivedData,
    OutboundCancelledData,
    OutboundClickedData,
    OutboundFailedData,
    OutboundOpenedData,
    OutboundScheduledData,
    OutboundSentData,
    WebhookEvent,
    WebhookTestData,
)


# ---------------------------------------------------------------------------
# EventType
# ---------------------------------------------------------------------------


class TestEventType:
    def test_values(self) -> None:
        assert EventType.OUTBOUND_SENT == "email.outbound.sent"
        assert EventType.OUTBOUND_FAILED == "email.outbound.failed"
        assert EventType.OUTBOUND_OPENED == "email.outbound.opened"
        assert EventType.OUTBOUND_CLICKED == "email.outbound.clicked"
        assert EventType.OUTBOUND_SCHEDULED == "email.outbound.scheduled"
        assert EventType.OUTBOUND_CANCELLED == "email.outbound.cancelled"
        assert EventType.INBOUND_RECEIVED == "email.inbound.received"
        assert EventType.DOMAIN_VERIFIED == "domain.verified"
        assert EventType.DOMAIN_FAILED == "domain.failed"
        assert EventType.WEBHOOK_TEST == "webhook.test"

    def test_str_comparison(self) -> None:
        assert EventType.INBOUND_RECEIVED == "email.inbound.received"
        assert "email.inbound.received" == EventType.INBOUND_RECEIVED

    def test_is_str_subclass(self) -> None:
        assert isinstance(EventType.INBOUND_RECEIVED, str)

    def test_from_string_value(self) -> None:
        assert EventType("email.outbound.sent") is EventType.OUTBOUND_SENT

    def test_invalid_value_raises(self) -> None:
        with pytest.raises(ValueError):
            EventType("not.a.real.event")


# ---------------------------------------------------------------------------
# WebhookEvent
# ---------------------------------------------------------------------------

SAMPLE_RAW = {
    "event_id": "evt-123",
    "event_type": "email.inbound.received",
    "timestamp": "2025-06-01T12:00:00Z",
    "data": {"from_email": "test@example.com", "subject": "Hello"},
}


class TestWebhookEvent:
    def test_from_dict(self) -> None:
        event = WebhookEvent.from_dict(SAMPLE_RAW)
        assert event.event_id == "evt-123"
        assert event.event_type is EventType.INBOUND_RECEIVED
        assert event.timestamp == datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        assert event.data["from_email"] == "test@example.com"

    def test_unknown_event_type_raises(self) -> None:
        raw = {**SAMPLE_RAW, "event_type": "unknown.event"}
        with pytest.raises(ValueError):
            WebhookEvent.from_dict(raw)

    def test_missing_event_id_raises(self) -> None:
        raw = {k: v for k, v in SAMPLE_RAW.items() if k != "event_id"}
        with pytest.raises(KeyError):
            WebhookEvent.from_dict(raw)

    def test_empty_data_defaults(self) -> None:
        raw = {k: v for k, v in SAMPLE_RAW.items() if k != "data"}
        event = WebhookEvent.from_dict(raw)
        assert event.data == {}

    def test_frozen(self) -> None:
        event = WebhookEvent.from_dict(SAMPLE_RAW)
        with pytest.raises(AttributeError):
            event.event_id = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Event-specific data models
# ---------------------------------------------------------------------------


class TestInboundReceivedData:
    def test_from_dict(self) -> None:
        data = InboundReceivedData.from_dict(
            {
                "email_id": "e1",
                "alias_id": "a1",
                "domain_id": "d1",
                "from_email": "sender@test.com",
                "alias": "alias@example.com",
                "subject": "Test",
                "attachment_count": 2,
                "body_preview": "Hello...",
                "received_at": "2025-06-01T12:00:00Z",
            }
        )
        assert data.email_id == "e1"
        assert data.alias == "alias@example.com"
        assert data.attachment_count == 2
        assert data.received_at == datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_optional_fields_default_none(self) -> None:
        data = InboundReceivedData.from_dict(
            {
                "email_id": "e1",
                "alias_id": "a1",
                "domain_id": "d1",
                "from_email": "sender@test.com",
                "alias": "alias@example.com",
                "subject": "Test",
                "attachment_count": 0,
            }
        )
        assert data.body_preview is None
        assert data.received_at is None


class TestOutboundSentData:
    def test_from_dict(self) -> None:
        data = OutboundSentData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "sent_at": "2025-06-01T12:00:00Z",
                "provider_message_id": "msg-xyz",
            }
        )
        assert data.email_id == "e1"
        assert data.sent_at == datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        assert data.provider_message_id == "msg-xyz"


class TestOutboundFailedData:
    def test_from_dict(self) -> None:
        data = OutboundFailedData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "error_message": "Bounced",
            }
        )
        assert data.error_message == "Bounced"

    def test_optional_error_message(self) -> None:
        data = OutboundFailedData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
            }
        )
        assert data.error_message is None


class TestOutboundOpenedData:
    def test_from_dict(self) -> None:
        data = OutboundOpenedData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "is_first_open": True,
                "is_bot": False,
                "open_count": 1,
                "opened_at": "2025-06-01T12:00:00Z",
            }
        )
        assert data.is_first_open is True
        assert data.is_bot is False
        assert data.open_count == 1


class TestOutboundClickedData:
    def test_from_dict(self) -> None:
        data = OutboundClickedData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "link_id": "lnk-1",
                "link_url": "https://example.com",
                "position": 0,
                "is_first_click": True,
                "is_bot": False,
                "link_click_count": 1,
                "link_unique_click_count": 1,
                "email_click_count": 1,
                "anchor_text": "Click here",
                "device_type": "desktop",
                "browser_name": "Chrome",
                "os_name": "Linux",
            }
        )
        assert data.link_id == "lnk-1"
        assert data.link_url == "https://example.com"
        assert data.anchor_text == "Click here"
        assert data.device_type == "desktop"


class TestOutboundScheduledData:
    def test_from_dict(self) -> None:
        data = OutboundScheduledData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "send_at": "2025-06-02T09:00:00Z",
                "send_at_timezone": "America/New_York",
                "send_at_utc": "2025-06-02T13:00:00Z",
            }
        )
        assert data.send_at_timezone == "America/New_York"


class TestOutboundCancelledData:
    def test_from_dict(self) -> None:
        data = OutboundCancelledData.from_dict(
            {
                "email_id": "e1",
                "from_email": "alias@example.com",
                "to_email": "user@test.com",
                "subject": "Hello",
                "cancelled_at": "2025-06-01T14:00:00Z",
            }
        )
        assert data.cancelled_at == datetime(2025, 6, 1, 14, 0, 0, tzinfo=timezone.utc)


class TestDomainVerifiedData:
    def test_from_dict(self) -> None:
        data = DomainVerifiedData.from_dict(
            {
                "domain_id": "d1",
                "domain": "example.com",
                "verified_at": "2025-06-01T12:00:00Z",
            }
        )
        assert data.domain == "example.com"
        assert data.verified_at is not None


class TestDomainFailedData:
    def test_from_dict(self) -> None:
        data = DomainFailedData.from_dict(
            {
                "domain_id": "d1",
                "domain": "example.com",
                "error": "DNS records not found",
            }
        )
        assert data.error == "DNS records not found"

    def test_optional_error(self) -> None:
        data = DomainFailedData.from_dict(
            {"domain_id": "d1", "domain": "example.com"}
        )
        assert data.error is None


class TestWebhookTestData:
    def test_from_dict(self) -> None:
        data = WebhookTestData.from_dict(
            {"webhook_id": "wh-1", "test": True}
        )
        assert data.webhook_id == "wh-1"
        assert data.test is True
