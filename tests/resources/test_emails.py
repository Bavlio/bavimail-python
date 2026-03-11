"""Tests for the Emails resource."""

from __future__ import annotations

import json

import httpx

from tests.conftest import (
    SAMPLE_BATCH_RESPONSE,
    SAMPLE_EMAIL,
    SAMPLE_EMAIL_CLICK,
    SAMPLE_TRACKED_LINK,
    json_response,
    make_client,
)


def test_send_email() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/emails" in str(request.url)
        body = request.content.decode()
        assert "user@test.com" in body
        return json_response(SAMPLE_EMAIL, status_code=200)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.send(
        alias_id=SAMPLE_EMAIL["alias_id"],
        to_email="user@test.com",
        subject="Test email",
        body="<p>Hello</p>",
    )
    assert email.to_email == "user@test.com"
    assert email.status == "sent"
    client.close()


def test_list_emails() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response([SAMPLE_EMAIL])

    client = make_client("https://test.com", "key", handler)
    emails = client.emails.list()
    assert len(emails) == 1
    client.close()


def test_list_emails_with_filters() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        assert "alias_id" in url_str
        assert "limit=10" in url_str
        return json_response([SAMPLE_EMAIL])

    client = make_client("https://test.com", "key", handler)
    emails = client.emails.list(alias_id="a1", limit=10, offset=0)
    assert len(emails) == 1
    client.close()


def test_get_email() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(SAMPLE_EMAIL)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.get(SAMPLE_EMAIL["id"])
    assert email.id == SAMPLE_EMAIL["id"]
    client.close()


def test_send_email_with_scheduling() -> None:
    scheduled_email = {
        **SAMPLE_EMAIL,
        "status": "queued",
        "send_at": "2025-02-01T10:00:00Z",
        "send_at_timezone": "America/New_York",
        "send_at_utc": "2025-02-01T15:00:00Z",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        body = json.loads(request.content)
        assert body["send_at"] == "2025-02-01T10:00:00"
        assert body["send_at_timezone"] == "America/New_York"
        return json_response(scheduled_email)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.send(
        alias_id=SAMPLE_EMAIL["alias_id"],
        to_email="user@test.com",
        subject="Scheduled",
        body="Hello",
        send_at="2025-02-01T10:00:00",
        send_at_timezone="America/New_York",
    )
    assert email.send_at is not None
    assert email.send_at_timezone == "America/New_York"
    client.close()


def test_send_email_with_click_tracking() -> None:
    tracked_email = {**SAMPLE_EMAIL, "track_clicks": True}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        body = json.loads(request.content)
        assert body["track_clicks"] is True
        return json_response(tracked_email)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.send(
        alias_id=SAMPLE_EMAIL["alias_id"],
        to_email="user@test.com",
        subject="Tracked",
        body="Hello",
        track_clicks=True,
    )
    assert email.track_clicks is True
    client.close()


def test_send_email_with_attachment_references() -> None:
    attachment_email = {
        **SAMPLE_EMAIL,
        "attachments": [
            {
                "id": "att-0000-0000-0000-000000000001",
                "filename": "invoice.pdf",
                "size_bytes": 1234,
                "mime_type": "application/pdf",
                "sha256": "abc123",
                "content_id": None,
                "is_inline": False,
            }
        ],
        "attachment_count": 1,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["attachments"] == [{"attachment_id": "att-0000-0000-0000-000000000001"}]
        return json_response(attachment_email)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.send(
        alias_id=SAMPLE_EMAIL["alias_id"],
        to_email="user@test.com",
        subject="Attachment refs",
        body="Hello",
        attachments=[{"attachment_id": "att-0000-0000-0000-000000000001"}],
    )
    assert email.attachment_count == 1
    assert email.attachments is not None
    assert email.attachments[0].id == "att-0000-0000-0000-000000000001"
    client.close()


def test_batch_send() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/emails/batch" in str(request.url)
        return json_response(SAMPLE_BATCH_RESPONSE)

    client = make_client("https://test.com", "key", handler)
    result = client.emails.batch_send([
        {"alias_id": "a1", "to_email": "user1@test.com", "subject": "Hi", "body": "Hello"},
        {"alias_id": "a1", "to_email": "bad-email", "subject": "Hi", "body": "Hello"},
    ])
    assert result.total == 2
    assert result.accepted == 1
    assert result.rejected == 1
    assert len(result.results) == 2
    assert result.results[0].email is not None
    assert result.results[1].error is not None
    client.close()


def test_cancel_email() -> None:
    cancelled = {**SAMPLE_EMAIL, "status": "cancelled", "cancelled_at": "2025-01-01T12:00:00Z"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/cancel" in str(request.url)
        return json_response(cancelled)

    client = make_client("https://test.com", "key", handler)
    email = client.emails.cancel(SAMPLE_EMAIL["id"])
    assert email.status == "cancelled"
    assert email.cancelled_at is not None
    client.close()


def test_list_clicks() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/clicks" in str(request.url)
        return json_response({"clicks": [SAMPLE_EMAIL_CLICK]})

    client = make_client("https://test.com", "key", handler)
    clicks = client.emails.list_clicks(SAMPLE_EMAIL["id"])
    assert len(clicks) == 1
    assert clicks[0].original_url == "https://example.com/page"
    assert clicks[0].is_first_click is True
    client.close()


def test_list_links() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/links" in str(request.url)
        return json_response([SAMPLE_TRACKED_LINK])

    client = make_client("https://test.com", "key", handler)
    links = client.emails.list_links(SAMPLE_EMAIL["id"])
    assert len(links) == 1
    assert links[0].original_url == "https://example.com/page"
    assert links[0].click_count == 5
    client.close()
