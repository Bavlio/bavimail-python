"""Tests for the Webhooks resource."""

from __future__ import annotations

import httpx

from tests.conftest import (
    SAMPLE_WEBHOOK,
    SAMPLE_WEBHOOK_CREATED,
    json_response,
    make_client,
    no_content_response,
)


def test_create_webhook() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        body = request.content.decode()
        assert "https://hooks.example.com" in body
        return json_response(SAMPLE_WEBHOOK_CREATED, status_code=200)

    client = make_client("https://test.com", "key", handler)
    wh = client.webhooks.create(
        "https://hooks.example.com/webhook",
        ["email.inbound.received"],
    )
    assert wh.secret == SAMPLE_WEBHOOK_CREATED["secret"]
    assert wh.is_verified is False
    client.close()


def test_list_webhooks() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response([SAMPLE_WEBHOOK])

    client = make_client("https://test.com", "key", handler)
    webhooks = client.webhooks.list()
    assert len(webhooks) == 1
    client.close()


def test_get_webhook() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(SAMPLE_WEBHOOK)

    client = make_client("https://test.com", "key", handler)
    wh = client.webhooks.get(SAMPLE_WEBHOOK["id"])
    assert wh.url == SAMPLE_WEBHOOK["url"]
    client.close()


def test_update_webhook() -> None:
    updated = {**SAMPLE_WEBHOOK, "is_active": False}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        return json_response(updated)

    client = make_client("https://test.com", "key", handler)
    wh = client.webhooks.update(SAMPLE_WEBHOOK["id"], is_active=False)
    assert wh.is_active is False
    client.close()


def test_delete_webhook() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.webhooks.delete(SAMPLE_WEBHOOK["id"])
    client.close()


def test_verify_webhook() -> None:
    verified = {**SAMPLE_WEBHOOK, "is_verified": True, "is_active": True}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/verify" in str(request.url)
        body = request.content.decode()
        assert "my-code" in body
        return json_response(verified)

    client = make_client("https://test.com", "key", handler)
    wh = client.webhooks.verify(SAMPLE_WEBHOOK["id"], "my-code")
    assert wh.is_verified is True
    client.close()


def test_resend_verification() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/resend-verification" in str(request.url)
        return json_response(SAMPLE_WEBHOOK)

    client = make_client("https://test.com", "key", handler)
    wh = client.webhooks.resend_verification(SAMPLE_WEBHOOK["id"])
    assert wh.id == SAMPLE_WEBHOOK["id"]
    client.close()


def test_test_webhook() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/test" in str(request.url)
        return json_response({"status": "test_event_enqueued"})

    client = make_client("https://test.com", "key", handler)
    result = client.webhooks.test(SAMPLE_WEBHOOK["id"])
    assert result["status"] == "test_event_enqueued"
    client.close()


def test_rotate_secret() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "/rotate-secret" in str(request.url)
        return json_response({"secret": "new-hex-secret"})

    client = make_client("https://test.com", "key", handler)
    result = client.webhooks.rotate_secret(SAMPLE_WEBHOOK["id"])
    assert result.secret == "new-hex-secret"
    client.close()
