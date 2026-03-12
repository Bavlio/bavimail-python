"""Tests for data model parsing."""

from __future__ import annotations

from bavimail.models.alias import Alias
from bavimail.models.email import (
    AttachmentMetadata,
    BatchEmailItemError,
    BatchEmailItemResult,
    BatchEmailResponse,
    EmailClick,
    TrackedLink,
)
from bavimail.models.conversation import ConversationDetail, ConversationSummary
from bavimail.models.domain import (
    DNSRecord,
    DNSRecordWithStatus,
    DNSVerificationResponse,
    Domain,
    DomainSetup,
)
from bavimail.models.email import Email
from bavimail.models.inbound_email import (
    InboundEmailDetail,
    InboundEmailSummary,
    Verdict,
)
from bavimail.models.tag import EmailTag, Tag
from bavimail.models.webhook import Webhook, WebhookCreated, WebhookSecret


def test_domain_from_dict() -> None:
    data = {
        "id": "d1",
        "domain": "example.com",
        "status": "verified",
        "is_active": True,
        "provider_key": "AWS",
        "user_id": "u1",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }
    domain = Domain.from_dict(data)
    assert domain.id == "d1"
    assert domain.domain == "example.com"
    assert domain.status == "verified"
    assert domain.created_at is not None


def test_domain_optional_fields_default_none() -> None:
    data = {
        "id": "d1",
        "domain": "example.com",
        "status": "pending",
        "is_active": True,
        "provider_key": "AWS",
        "user_id": "u1",
    }
    domain = Domain.from_dict(data)
    assert domain.verified_at is None
    assert domain.ses_verification_token is None
    assert domain.strip_tracking_on_read is False


def test_dns_record_from_dict() -> None:
    data = {"type": "TXT", "name": "_amazonses.example.com", "value": "abc123"}
    record = DNSRecord.from_dict(data)
    assert record.type == "TXT"
    assert record.priority is None


def test_dns_record_with_status_from_dict() -> None:
    data = {
        "type": "CNAME",
        "name": "tok._domainkey.example.com",
        "value": "tok.dkim.amazonses.com",
        "status": "verified",
        "last_checked": "2025-01-01T12:00:00Z",
    }
    record = DNSRecordWithStatus.from_dict(data)
    assert record.status == "verified"
    assert record.last_checked is not None


def test_dns_verification_response_from_dict() -> None:
    data = {
        "domain": "example.com",
        "overall_progress": {
            "total_records": 5,
            "verified": 3,
            "not_configured": 1,
            "incorrect": 0,
            "errors": 1,
        },
        "records": [],
        "last_checked": "2025-01-01T12:00:00Z",
    }
    resp = DNSVerificationResponse.from_dict(data)
    assert resp.overall_progress.total_records == 5
    assert resp.mail_from_status is None


def test_domain_setup_from_dict() -> None:
    data = {
        "domain": "example.com",
        "dns_records": [
            {"type": "TXT", "name": "example.com", "value": "v=spf1..."},
        ],
        "verification_instructions": "Add these records",
    }
    setup = DomainSetup.from_dict(data)
    assert len(setup.dns_records) == 1


def test_alias_from_dict() -> None:
    data = {
        "id": "a1",
        "domain_id": "d1",
        "alias": "support",
        "full_email": "support@example.com",
        "domain_name": "example.com",
        "user_id": "u1",
    }
    alias = Alias.from_dict(data)
    assert alias.full_email == "support@example.com"


def test_email_from_dict() -> None:
    data = {
        "id": "e1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "support@example.com",
        "to_email": "user@test.com",
        "subject": "Test",
        "body_text": "Hello",
        "status": "sent",
        "provider_message_id": "msg-1",
        "user_id": "u1",
        "track_opens": True,
        "open_count": 2,
        "first_opened_at": "2025-01-02T00:00:00Z",
    }
    email = Email.from_dict(data)
    assert email.open_count == 2
    assert email.first_opened_at is not None


def test_email_from_dict_with_warmup_fields() -> None:
    data = {
        "id": "e1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "support@example.com",
        "to_email": "user@test.com",
        "subject": "Test",
        "body_text": "Hello",
        "status": "sent",
        "provider_message_id": "msg-1",
        "user_id": "u1",
        "warmup_suspicious": True,
        "warmup_suspicious_tokens": ["motor-graph", "river-stone"],
    }
    email = Email.from_dict(data)
    assert email.warmup_suspicious is True
    assert email.warmup_suspicious_tokens == ["motor-graph", "river-stone"]


def test_email_with_attachments() -> None:
    data = {
        "id": "e1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "support@example.com",
        "to_email": "user@test.com",
        "subject": "Test",
        "body_text": "Hello",
        "status": "sent",
        "provider_message_id": "msg-1",
        "user_id": "u1",
        "attachments": [
            {
                "filename": "doc.pdf",
                "size_bytes": 1024,
                "mime_type": "application/pdf",
            }
        ],
    }
    email = Email.from_dict(data)
    assert email.attachments is not None
    assert len(email.attachments) == 1
    assert email.attachments[0].filename == "doc.pdf"


def test_inbound_email_summary_from_dict() -> None:
    data = {
        "id": "i1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "sender@other.com",
        "subject": "Hi",
        "alias_name": "support",
        "domain_name": "example.com",
        "full_email": "support@example.com",
        "attachment_count": 0,
        "has_html": True,
        "provider_message_id": "inb-1",
        "raw_email_uri": "s3://bucket/key",
        "user_id": "u1",
        "tags": [
            {"id": "t1", "name": "important", "type": "tag"},
        ],
    }
    summary = InboundEmailSummary.from_dict(data)
    assert summary.from_email == "sender@other.com"
    assert summary.tags is not None
    assert len(summary.tags) == 1


def test_inbound_email_detail_from_dict() -> None:
    data = {
        "id": "i1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "sender@other.com",
        "to_email": "support@example.com",
        "subject": "Hi",
        "alias_name": "support",
        "domain_name": "example.com",
        "full_email": "support@example.com",
        "attachment_count": 1,
        "has_html": True,
        "provider_message_id": "inb-1",
        "raw_email_uri": "s3://bucket/key",
        "user_id": "u1",
        "cc_emails": [{"email": "copy@example.com", "name": "Copy"}],
        "headers": [{"name": "Subject", "value": "Hi"}],
        "body_text": "Hello",
        "spam_verdict": {"status": "PASS"},
        "dkim_verdict": {"status": "PASS", "details": "selector1"},
        "attachments": [
            {
                "filename": "photo.jpg",
                "size_bytes": 5000,
                "mime_type": "image/jpeg",
                "is_inline": False,
            }
        ],
    }
    detail = InboundEmailDetail.from_dict(data)
    assert detail.spam_verdict is not None
    assert detail.spam_verdict.status == "PASS"
    assert detail.attachments is not None
    assert len(detail.attachments) == 1
    assert detail.cc_emails is not None
    assert detail.cc_emails[0].email == "copy@example.com"
    assert detail.headers is not None
    assert detail.headers[0].name == "Subject"


def test_verdict_from_dict_none() -> None:
    assert Verdict.from_dict(None) is None


def test_conversation_summary_from_dict() -> None:
    data = {
        "id": "c1",
        "subject": "Thread",
        "message_count": 3,
        "user_id": "u1",
        "first_message_at": "2025-01-01T00:00:00Z",
        "last_message_at": "2025-01-03T00:00:00Z",
    }
    conv = ConversationSummary.from_dict(data)
    assert conv.message_count == 3


def test_conversation_detail_from_dict() -> None:
    data = {
        "id": "c1",
        "subject": "Thread",
        "message_count": 1,
        "user_id": "u1",
        "messages": [
            {
                "id": "m1",
                "direction": "inbound",
                "from_email": "sender@test.com",
                "to_email": "support@example.com",
                "subject": "Hi",
                "attachment_count": 0,
                "timestamp": "2025-01-01T00:00:00Z",
            }
        ],
    }
    detail = ConversationDetail.from_dict(data)
    assert len(detail.messages) == 1
    assert detail.messages[0].direction == "inbound"


def test_tag_from_dict() -> None:
    data = {
        "id": "t1",
        "name": "urgent",
        "type": "tag",
        "sort_order": 1,
        "is_pinned": True,
        "is_system": False,
        "email_count": 10,
        "is_visible": True,
        "user_id": "u1",
        "color": "#ff0000",
    }
    tag = Tag.from_dict(data)
    assert tag.color == "#ff0000"
    assert tag.is_pinned is True


def test_email_tag_from_dict() -> None:
    data = {
        "tag": {"id": "t1", "name": "important", "type": "tag"},
        "tagged_by": "user",
        "tagged_at": "2025-01-01T00:00:00Z",
        "note": "Flagged manually",
    }
    et = EmailTag.from_dict(data)
    assert et.tag.name == "important"
    assert et.note == "Flagged manually"


def test_webhook_from_dict() -> None:
    data = {
        "id": "w1",
        "url": "https://hooks.example.com/wh",
        "event_types": ["email.inbound.received"],
        "is_active": True,
        "is_verified": True,
        "consecutive_failures": 0,
    }
    wh = Webhook.from_dict(data)
    assert wh.url == "https://hooks.example.com/wh"


def test_webhook_created_from_dict() -> None:
    data = {
        "id": "w1",
        "url": "https://hooks.example.com/wh",
        "secret": "abcdef",
        "event_types": ["domain.verified"],
        "is_active": False,
        "is_verified": False,
    }
    wh = WebhookCreated.from_dict(data)
    assert wh.secret == "abcdef"


def test_webhook_secret_from_dict() -> None:
    ws = WebhookSecret.from_dict({"secret": "newsecret"})
    assert ws.secret == "newsecret"


def test_datetime_parsing_with_z_suffix() -> None:
    data = {
        "id": "d1",
        "domain": "example.com",
        "status": "verified",
        "is_active": True,
        "provider_key": "AWS",
        "user_id": "u1",
        "verified_at": "2025-06-15T10:30:00Z",
    }
    domain = Domain.from_dict(data)
    assert domain.verified_at is not None
    assert domain.verified_at.year == 2025


def test_datetime_parsing_with_offset() -> None:
    data = {
        "id": "d1",
        "domain": "example.com",
        "status": "verified",
        "is_active": True,
        "provider_key": "AWS",
        "user_id": "u1",
        "verified_at": "2025-06-15T10:30:00+02:00",
    }
    domain = Domain.from_dict(data)
    assert domain.verified_at is not None


def test_email_from_dict_with_click_tracking_fields() -> None:
    data = {
        "id": "e1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "support@example.com",
        "to_email": "user@test.com",
        "subject": "Test",
        "body_text": "Hello",
        "status": "sent",
        "provider_message_id": "msg-1",
        "user_id": "u1",
        "track_clicks": True,
        "click_count": 5,
        "first_clicked_at": "2025-01-02T00:00:00Z",
        "last_clicked_at": "2025-01-03T00:00:00Z",
        "tracked_links_count": 2,
    }
    email = Email.from_dict(data)
    assert email.track_clicks is True
    assert email.click_count == 5
    assert email.first_clicked_at is not None
    assert email.last_clicked_at is not None
    assert email.tracked_links_count == 2


def test_email_from_dict_with_scheduling_fields() -> None:
    data = {
        "id": "e1",
        "alias_id": "a1",
        "domain_id": "d1",
        "from_email": "support@example.com",
        "to_email": "user@test.com",
        "subject": "Test",
        "body_text": "Hello",
        "status": "queued",
        "provider_message_id": "msg-1",
        "user_id": "u1",
        "send_at": "2025-02-01T10:00:00Z",
        "send_at_timezone": "America/New_York",
        "send_at_utc": "2025-02-01T15:00:00Z",
        "cancelled_at": None,
    }
    email = Email.from_dict(data)
    assert email.send_at is not None
    assert email.send_at_timezone == "America/New_York"
    assert email.send_at_utc is not None
    assert email.cancelled_at is None


def test_attachment_metadata_nullable_filename() -> None:
    data = {
        "filename": None,
        "size_bytes": 512,
        "mime_type": "application/octet-stream",
        "is_inline": True,
    }
    att = AttachmentMetadata.from_dict(data)
    assert att.filename is None
    assert att.is_inline is True
    assert att.size_bytes == 512


def test_email_click_from_dict() -> None:
    data = {
        "id": "clk-1",
        "link_id": "lnk-1",
        "original_url": "https://example.com",
        "position": 0,
        "clicked_at": "2025-01-02T10:00:00Z",
        "created_at": "2025-01-02T10:00:00Z",
        "user_agent": "Mozilla/5.0",
        "ip_address": "192.168.1.1",
        "device_type": "desktop",
        "browser_name": "Chrome",
        "os_name": "Windows",
        "is_first_click": True,
        "is_bot": False,
    }
    click = EmailClick.from_dict(data)
    assert click.id == "clk-1"
    assert click.original_url == "https://example.com"
    assert click.clicked_at is not None
    assert click.is_first_click is True
    assert click.is_bot is False
    assert click.browser_name == "Chrome"


def test_tracked_link_from_dict() -> None:
    data = {
        "id": "tl-1",
        "link_id": "lnk-1",
        "original_url": "https://example.com",
        "position": 0,
        "anchor_text": "Click here",
        "click_count": 5,
        "unique_click_count": 3,
        "first_clicked_at": "2025-01-02T10:00:00Z",
        "last_clicked_at": "2025-01-03T14:00:00Z",
    }
    link = TrackedLink.from_dict(data)
    assert link.id == "tl-1"
    assert link.anchor_text == "Click here"
    assert link.click_count == 5
    assert link.unique_click_count == 3
    assert link.first_clicked_at is not None


def test_batch_email_item_error_from_dict() -> None:
    data = {"message": "Invalid recipient", "code": "INVALID_RECIPIENT", "category": "validation"}
    err = BatchEmailItemError.from_dict(data)
    assert err.message == "Invalid recipient"
    assert err.code == "INVALID_RECIPIENT"
    assert err.category == "validation"


def test_batch_email_item_result_from_dict() -> None:
    data = {
        "index": 0,
        "status": "accepted",
        "email": {
            "id": "e1",
            "alias_id": "a1",
            "domain_id": "d1",
            "from_email": "support@example.com",
            "to_email": "user@test.com",
            "subject": "Test",
            "body_text": "Hello",
            "status": "queued",
            "provider_message_id": "msg-1",
            "user_id": "u1",
        },
    }
    result = BatchEmailItemResult.from_dict(data)
    assert result.index == 0
    assert result.status == "accepted"
    assert result.email is not None
    assert result.email.id == "e1"
    assert result.error is None


def test_batch_email_response_from_dict() -> None:
    data = {
        "total": 2,
        "accepted": 1,
        "rejected": 1,
        "results": [
            {
                "index": 0,
                "status": "accepted",
                "email": {
                    "id": "e1",
                    "alias_id": "a1",
                    "domain_id": "d1",
                    "from_email": "support@example.com",
                    "to_email": "user@test.com",
                    "subject": "Test",
                    "body_text": "Hello",
                    "status": "queued",
                    "provider_message_id": "msg-1",
                    "user_id": "u1",
                },
            },
            {
                "index": 1,
                "status": "rejected",
                "error": {"message": "Invalid recipient"},
            },
        ],
    }
    resp = BatchEmailResponse.from_dict(data)
    assert resp.total == 2
    assert resp.accepted == 1
    assert resp.rejected == 1
    assert len(resp.results) == 2
    assert resp.results[0].email is not None
    assert resp.results[1].error is not None
    assert resp.results[1].error.message == "Invalid recipient"


def test_alias_from_dict_with_signature() -> None:
    data = {
        "id": "a1",
        "domain_id": "d1",
        "alias": "support",
        "full_email": "support@example.com",
        "domain_name": "example.com",
        "user_id": "u1",
        "signature_html": "<p>Best regards</p>",
        "signature_text": "Best regards",
    }
    alias = Alias.from_dict(data)
    assert alias.signature_html == "<p>Best regards</p>"
    assert alias.signature_text == "Best regards"


def test_alias_from_dict_with_warmup_token() -> None:
    data = {
        "id": "a1",
        "domain_id": "d1",
        "alias": "support",
        "full_email": "support@example.com",
        "domain_name": "example.com",
        "user_id": "u1",
        "warmup_token": "motor-graph",
    }
    alias = Alias.from_dict(data)
    assert alias.warmup_token == "motor-graph"
