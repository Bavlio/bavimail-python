"""Tests for the Emails resource."""

from __future__ import annotations

import httpx

from tests.conftest import SAMPLE_EMAIL, json_response, make_client


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
