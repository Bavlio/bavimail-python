"""Tests for the FastAPI webhook router integration."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

import httpx
import pytest

from bavimail.events import EventType, WebhookEvent
from bavimail.integrations.fastapi import create_webhook_router

SECRET_HEX = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

SAMPLE_EVENT = {
    "event_id": "evt-fastapi-001",
    "event_type": "email.inbound.received",
    "timestamp": "2025-06-01T12:00:00Z",
    "data": {"from_email": "test@example.com", "subject": "Hello"},
}


def _sign(payload: bytes, secret: str = SECRET_HEX) -> tuple[str, str]:
    ts = str(int(time.time()))
    signing_string = f"{ts}.{payload.decode()}"
    sig = hmac.new(
        bytes.fromhex(secret),
        signing_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    return sig, ts


@pytest.fixture()
def fastapi_app() -> Any:
    fastapi = pytest.importorskip("fastapi")
    app = fastapi.FastAPI()
    results: list[str] = []

    def handler(event: WebhookEvent) -> None:
        results.append(event.event_id)

    router = create_webhook_router(
        handlers={EventType.INBOUND_RECEIVED: [handler]},
        secret=SECRET_HEX,
        path="/webhooks",
    )
    app.include_router(router)
    app.state.results = results
    return app


async def test_health_check(fastapi_app: Any) -> None:
    transport = httpx.ASGITransport(app=fastapi_app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/webhooks")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


async def test_valid_webhook(fastapi_app: Any) -> None:
    body = json.dumps(SAMPLE_EVENT).encode()
    sig, ts = _sign(body)
    transport = httpx.ASGITransport(app=fastapi_app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post(
            "/webhooks",
            content=body,
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
    assert fastapi_app.state.results == ["evt-fastapi-001"]


async def test_invalid_signature(fastapi_app: Any) -> None:
    body = json.dumps(SAMPLE_EVENT).encode()
    transport = httpx.ASGITransport(app=fastapi_app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post(
            "/webhooks",
            content=body,
            headers={
                "x-webhook-signature": "bad",
                "x-webhook-timestamp": str(int(time.time())),
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 403


async def test_invalid_json(fastapi_app: Any) -> None:
    body = b"not json"
    sig, ts = _sign(body)
    transport = httpx.ASGITransport(app=fastapi_app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post(
            "/webhooks",
            content=body,
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 400


async def test_async_handler(fastapi_app: Any) -> None:
    """Test that async handlers work in FastAPI context."""
    fastapi = pytest.importorskip("fastapi")
    app = fastapi.FastAPI()
    results: list[str] = []

    async def async_handler(event: WebhookEvent) -> None:
        results.append("async-" + event.event_id)

    router = create_webhook_router(
        handlers={EventType.INBOUND_RECEIVED: [async_handler]},
        secret=SECRET_HEX,
        path="/webhooks",
    )
    app.include_router(router)

    body = json.dumps(SAMPLE_EVENT).encode()
    sig, ts = _sign(body)
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post(
            "/webhooks",
            content=body,
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 200
    assert results == ["async-evt-fastapi-001"]


async def test_handler_error_still_returns_200() -> None:
    fastapi = pytest.importorskip("fastapi")
    app = fastapi.FastAPI()

    def bad_handler(event: WebhookEvent) -> None:
        raise RuntimeError("boom")

    router = create_webhook_router(
        handlers={EventType.INBOUND_RECEIVED: [bad_handler]},
        secret=SECRET_HEX,
        path="/webhooks",
    )
    app.include_router(router)

    body = json.dumps(SAMPLE_EVENT).encode()
    sig, ts = _sign(body)
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post(
            "/webhooks",
            content=body,
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 200
