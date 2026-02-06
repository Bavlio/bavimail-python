"""Shared test fixtures."""

from __future__ import annotations

import json
from typing import Any, Callable

import httpx
import pytest

from bavimail import Bavimail


def make_mock_transport(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.MockTransport:
    """Create a mock transport from a handler function."""
    return httpx.MockTransport(handler)


def json_response(
    data: Any,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Build a JSON response for mock transport."""
    resp_headers = {"content-type": "application/json", "x-request-id": "test-req-id"}
    if headers:
        resp_headers.update(headers)
    return httpx.Response(
        status_code=status_code,
        content=json.dumps(data).encode(),
        headers=resp_headers,
    )


def no_content_response() -> httpx.Response:
    """Build a 204 No Content response."""
    return httpx.Response(status_code=204, headers={"x-request-id": "test-req-id"})


def error_response(
    status_code: int,
    message: str = "Error",
    code: str | None = None,
    category: str | None = None,
) -> httpx.Response:
    """Build an error response for mock transport."""
    detail: dict[str, Any] = {"message": message}
    if code:
        detail["code"] = code
    if category:
        detail["category"] = category
    return json_response({"detail": detail}, status_code=status_code)


SAMPLE_DOMAIN: dict[str, Any] = {
    "id": "d1000000-0000-0000-0000-000000000001",
    "domain": "example.com",
    "status": "verified",
    "is_active": True,
    "provider_key": "AWS",
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "strip_tracking_on_read": False,
}

SAMPLE_ALIAS: dict[str, Any] = {
    "id": "a1000000-0000-0000-0000-000000000001",
    "domain_id": "d1000000-0000-0000-0000-000000000001",
    "alias": "support",
    "full_email": "support@example.com",
    "domain_name": "example.com",
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

SAMPLE_EMAIL: dict[str, Any] = {
    "id": "e1000000-0000-0000-0000-000000000001",
    "alias_id": "a1000000-0000-0000-0000-000000000001",
    "domain_id": "d1000000-0000-0000-0000-000000000001",
    "from_email": "support@example.com",
    "to_email": "user@test.com",
    "subject": "Test email",
    "body_text": "Hello",
    "body_html": "<p>Hello</p>",
    "status": "sent",
    "provider_message_id": "msg-123",
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "track_opens": True,
    "open_count": 0,
    "attachment_count": 0,
    "track_clicks": False,
    "click_count": 0,
    "tracked_links_count": 0,
}

SAMPLE_EMAIL_CLICK: dict[str, Any] = {
    "id": "clk-0000-0000-0000-000000000001",
    "link_id": "lnk-0000-0000-0000-000000000001",
    "original_url": "https://example.com/page",
    "position": 0,
    "clicked_at": "2025-01-02T10:00:00Z",
    "created_at": "2025-01-02T10:00:00Z",
    "updated_at": "2025-01-02T10:00:00Z",
    "user_agent": "Mozilla/5.0",
    "ip_address": "192.168.1.1",
    "device_type": "desktop",
    "browser_name": "Chrome",
    "os_name": "Windows",
    "is_first_click": True,
    "is_bot": False,
}

SAMPLE_TRACKED_LINK: dict[str, Any] = {
    "id": "tl-0000-0000-0000-000000000001",
    "link_id": "lnk-0000-0000-0000-000000000001",
    "original_url": "https://example.com/page",
    "position": 0,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "anchor_text": "Click here",
    "click_count": 5,
    "unique_click_count": 3,
    "first_clicked_at": "2025-01-02T10:00:00Z",
    "last_clicked_at": "2025-01-03T14:00:00Z",
}

SAMPLE_BATCH_RESPONSE: dict[str, Any] = {
    "total": 2,
    "accepted": 1,
    "rejected": 1,
    "results": [
        {
            "index": 0,
            "status": "accepted",
            "email": {
                "id": "e1000000-0000-0000-0000-000000000001",
                "alias_id": "a1000000-0000-0000-0000-000000000001",
                "domain_id": "d1000000-0000-0000-0000-000000000001",
                "from_email": "support@example.com",
                "to_email": "user@test.com",
                "subject": "Test email",
                "body_text": "Hello",
                "status": "queued",
                "provider_message_id": "msg-123",
                "user_id": "u1000000-0000-0000-0000-000000000001",
            },
        },
        {
            "index": 1,
            "status": "rejected",
            "error": {
                "message": "Invalid recipient",
                "code": "INVALID_RECIPIENT",
                "category": "validation",
            },
        },
    ],
}

SAMPLE_INBOUND_SUMMARY: dict[str, Any] = {
    "id": "i1000000-0000-0000-0000-000000000001",
    "alias_id": "a1000000-0000-0000-0000-000000000001",
    "domain_id": "d1000000-0000-0000-0000-000000000001",
    "from_email": "sender@other.com",
    "subject": "Inbound test",
    "alias_name": "support",
    "domain_name": "example.com",
    "full_email": "support@example.com",
    "attachment_count": 0,
    "has_html": True,
    "provider_message_id": "inb-123",
    "raw_email_uri": "s3://bucket/key",
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "provider_received_at": "2025-01-01T00:00:00Z",
}

SAMPLE_INBOUND_DETAIL: dict[str, Any] = {
    **SAMPLE_INBOUND_SUMMARY,
    "to_email": "support@example.com",
    "body_text": "Hello from sender",
    "body_html": "<p>Hello from sender</p>",
}

SAMPLE_CONVERSATION: dict[str, Any] = {
    "id": "c1000000-0000-0000-0000-000000000001",
    "subject": "Test conversation",
    "message_count": 2,
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "first_message_at": "2025-01-01T00:00:00Z",
    "last_message_at": "2025-01-02T00:00:00Z",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-02T00:00:00Z",
}

SAMPLE_TAG: dict[str, Any] = {
    "id": "t1000000-0000-0000-0000-000000000001",
    "name": "important",
    "type": "tag",
    "sort_order": 0,
    "is_pinned": False,
    "is_system": False,
    "email_count": 5,
    "is_visible": True,
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

SAMPLE_WEBHOOK: dict[str, Any] = {
    "id": "w1000000-0000-0000-0000-000000000001",
    "url": "https://hooks.example.com/webhook",
    "event_types": ["email.inbound.received"],
    "is_active": True,
    "is_verified": True,
    "consecutive_failures": 0,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

SAMPLE_WEBHOOK_CREATED: dict[str, Any] = {
    **SAMPLE_WEBHOOK,
    "secret": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    "is_active": False,
    "is_verified": False,
}


@pytest.fixture()
def base_url() -> str:
    return "https://api.bavimail.test"


@pytest.fixture()
def api_key() -> str:
    return "bvm_test_key_12345"


def make_client(
    base_url: str,
    api_key: str,
    handler: Callable[[httpx.Request], httpx.Response],
) -> Bavimail:
    """Create a Bavimail client with a mock transport."""
    transport = make_mock_transport(handler)
    sync_client = httpx.Client(
        transport=transport,
        base_url=base_url,
        headers={
            "x-api-key": api_key,
            "User-Agent": "bavimail-python/test",
            "Accept": "application/json",
        },
    )
    return Bavimail(
        api_key=api_key,
        base_url=base_url,
        http_client=sync_client,
    )


def make_async_client(
    base_url: str,
    api_key: str,
    handler: Callable[[httpx.Request], httpx.Response],
) -> Bavimail:
    """Create a Bavimail client with an async mock transport."""
    transport = make_mock_transport(handler)
    async_client = httpx.AsyncClient(
        transport=transport,
        base_url=base_url,
        headers={
            "x-api-key": api_key,
            "User-Agent": "bavimail-python/test",
            "Accept": "application/json",
        },
    )
    return Bavimail(
        api_key=api_key,
        base_url=base_url,
        async_http_client=async_client,
    )
