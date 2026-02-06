"""Tests for the InboundEmails resource."""

from __future__ import annotations

import httpx

from tests.conftest import (
    SAMPLE_INBOUND_DETAIL,
    SAMPLE_INBOUND_SUMMARY,
    json_response,
    make_client,
    no_content_response,
)


def test_list_inbound_emails() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return json_response([SAMPLE_INBOUND_SUMMARY])

    client = make_client("https://test.com", "key", handler)
    emails = client.inbound_emails.list()
    assert len(emails) == 1
    assert emails[0].from_email == "sender@other.com"
    client.close()


def test_get_inbound_email() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(SAMPLE_INBOUND_DETAIL)

    client = make_client("https://test.com", "key", handler)
    email = client.inbound_emails.get(SAMPLE_INBOUND_DETAIL["id"])
    assert email.to_email == "support@example.com"
    client.close()


def test_download_raw() -> None:
    raw_content = b"From: sender@test.com\r\nSubject: Test\r\n\r\nBody"

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/raw" in str(request.url)
        return httpx.Response(200, content=raw_content)

    client = make_client("https://test.com", "key", handler)
    data = client.inbound_emails.download_raw(SAMPLE_INBOUND_DETAIL["id"])
    assert data == raw_content
    client.close()


def test_download_attachment() -> None:
    attachment_bytes = b"PDF content here"

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/attachments/0" in str(request.url)
        return httpx.Response(200, content=attachment_bytes)

    client = make_client("https://test.com", "key", handler)
    data = client.inbound_emails.download_attachment(SAMPLE_INBOUND_DETAIL["id"], 0)
    assert data == attachment_bytes
    client.close()


def test_delete_inbound_email() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.inbound_emails.delete(SAMPLE_INBOUND_DETAIL["id"])
    client.close()


def test_add_tags() -> None:
    tag_response = [
        {
            "tag": {"id": "t1", "name": "urgent", "type": "tag"},
            "tagged_by": "user",
            "tagged_at": "2025-01-01T00:00:00Z",
        }
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/tags" in str(request.url)
        return json_response(tag_response)

    client = make_client("https://test.com", "key", handler)
    tags = client.inbound_emails.add_tags(SAMPLE_INBOUND_DETAIL["id"], ["t1"])
    assert len(tags) == 1
    assert tags[0].tag.name == "urgent"
    client.close()


def test_get_tags() -> None:
    tag_response = [
        {
            "tag": {"id": "t1", "name": "urgent", "type": "tag"},
            "tagged_by": "user",
            "tagged_at": "2025-01-01T00:00:00Z",
        }
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert "/tags" in str(request.url)
        return json_response(tag_response)

    client = make_client("https://test.com", "key", handler)
    tags = client.inbound_emails.get_tags(SAMPLE_INBOUND_DETAIL["id"])
    assert len(tags) == 1
    client.close()


def test_remove_tag() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        assert "/tags/t1" in str(request.url)
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.inbound_emails.remove_tag(SAMPLE_INBOUND_DETAIL["id"], "t1")
    client.close()
