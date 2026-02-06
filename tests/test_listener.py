"""Tests for the ASGI webhook app and listen() orchestration."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from bavimail import Bavimail, EventType
from bavimail._listener import WebhookApp
from bavimail.events import WebhookEvent

SECRET_HEX = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"


def _make_signed_request(
    payload: dict[str, Any],
    secret: str = SECRET_HEX,
) -> tuple[bytes, dict[str, str]]:
    """Build a signed webhook payload and headers."""
    body = json.dumps(payload).encode()
    ts = str(int(time.time()))
    signing_string = f"{ts}.{body.decode()}"
    sig = hmac.new(
        bytes.fromhex(secret),
        signing_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    headers = {
        "x-webhook-signature": sig,
        "x-webhook-timestamp": ts,
        "content-type": "application/json",
    }
    return body, headers


SAMPLE_EVENT = {
    "event_id": "evt-001",
    "event_type": "email.inbound.received",
    "timestamp": "2025-06-01T12:00:00Z",
    "data": {"from_email": "test@example.com", "subject": "Hello"},
}


# ---------------------------------------------------------------------------
# ASGI app tests via httpx.ASGITransport
# ---------------------------------------------------------------------------


def _build_app(
    handlers: dict[EventType, list[Any]] | None = None,
    on_error: Any = None,
) -> WebhookApp:
    if handlers is None:
        handlers = {EventType.INBOUND_RECEIVED: [lambda e: None]}
    return WebhookApp(
        handlers=handlers,
        secret=SECRET_HEX,
        path="/webhooks",
        on_error=on_error,
    )


@pytest.fixture()
def asgi_client() -> httpx.AsyncClient:
    app = _build_app()
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")


async def test_health_check(asgi_client: httpx.AsyncClient) -> None:
    resp = await asgi_client.get("/webhooks")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_valid_webhook_dispatch(asgi_client: httpx.AsyncClient) -> None:
    body, headers = _make_signed_request(SAMPLE_EVENT)
    resp = await asgi_client.post("/webhooks", content=body, headers=headers)
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_invalid_signature_returns_403(asgi_client: httpx.AsyncClient) -> None:
    body = json.dumps(SAMPLE_EVENT).encode()
    headers = {
        "x-webhook-signature": "invalidsig",
        "x-webhook-timestamp": str(int(time.time())),
        "content-type": "application/json",
    }
    resp = await asgi_client.post("/webhooks", content=body, headers=headers)
    assert resp.status_code == 403


async def test_bad_json_returns_400() -> None:
    app = _build_app()
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        ts = str(int(time.time()))
        bad_body = b"not json"
        signing_string = f"{ts}.{bad_body.decode()}"
        sig = hmac.new(
            bytes.fromhex(SECRET_HEX),
            signing_string.encode(),
            hashlib.sha256,
        ).hexdigest()
        resp = await client.post(
            "/webhooks",
            content=bad_body,
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
                "content-type": "application/json",
            },
        )
        assert resp.status_code == 400


async def test_wrong_path_returns_404(asgi_client: httpx.AsyncClient) -> None:
    resp = await asgi_client.get("/wrong-path")
    assert resp.status_code == 404


async def test_multiple_handlers_all_called() -> None:
    results: list[str] = []

    def handler_a(event: WebhookEvent) -> None:
        results.append("a")

    def handler_b(event: WebhookEvent) -> None:
        results.append("b")

    app = _build_app(handlers={EventType.INBOUND_RECEIVED: [handler_a, handler_b]})
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        body, headers = _make_signed_request(SAMPLE_EVENT)
        resp = await client.post("/webhooks", content=body, headers=headers)
        assert resp.status_code == 200
    assert results == ["a", "b"]


async def test_async_handler() -> None:
    results: list[str] = []

    async def async_handler(event: WebhookEvent) -> None:
        results.append("async")

    app = _build_app(handlers={EventType.INBOUND_RECEIVED: [async_handler]})
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        body, headers = _make_signed_request(SAMPLE_EVENT)
        resp = await client.post("/webhooks", content=body, headers=headers)
        assert resp.status_code == 200
    assert results == ["async"]


async def test_handler_error_still_returns_200() -> None:
    def bad_handler(event: WebhookEvent) -> None:
        raise RuntimeError("oops")

    app = _build_app(handlers={EventType.INBOUND_RECEIVED: [bad_handler]})
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        body, headers = _make_signed_request(SAMPLE_EVENT)
        resp = await client.post("/webhooks", content=body, headers=headers)
        assert resp.status_code == 200


async def test_on_error_callback_invoked() -> None:
    captured: list[tuple[Exception, WebhookEvent]] = []

    def on_error(exc: Exception, event: WebhookEvent) -> None:
        captured.append((exc, event))

    def bad_handler(event: WebhookEvent) -> None:
        raise RuntimeError("boom")

    app = _build_app(
        handlers={EventType.INBOUND_RECEIVED: [bad_handler]},
        on_error=on_error,
    )
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        body, headers = _make_signed_request(SAMPLE_EVENT)
        await client.post("/webhooks", content=body, headers=headers)
    assert len(captured) == 1
    assert isinstance(captured[0][0], RuntimeError)
    assert captured[0][1].event_id == "evt-001"


async def test_invalid_event_payload_returns_400() -> None:
    """Valid JSON but not a valid webhook event structure."""
    app = _build_app()
    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        body, headers = _make_signed_request({"not": "an event"})
        resp = await client.post("/webhooks", content=body, headers=headers)
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# listen() orchestration tests
# ---------------------------------------------------------------------------


class TestListenOrchestration:
    def test_listen_no_handlers_raises(self) -> None:
        client = Bavimail(api_key="bvm_test")
        with pytest.raises(ValueError, match="No event handlers"):
            client.listen(port=8080, secret="abc123")

    def test_listen_no_url_or_secret_raises(self) -> None:
        client = Bavimail(api_key="bvm_test")

        @client.on(EventType.INBOUND_RECEIVED)
        def handler(event: WebhookEvent) -> None:
            pass

        with pytest.raises(ValueError, match="webhook_url.*secret"):
            client.listen(port=8080)

    def test_listen_missing_uvicorn_raises(self) -> None:
        client = Bavimail(api_key="bvm_test")

        @client.on(EventType.INBOUND_RECEIVED)
        def handler(event: WebhookEvent) -> None:
            pass

        with patch.dict("sys.modules", {"uvicorn": None}):
            with pytest.raises(ImportError, match="uvicorn"):
                client.listen(port=8080, secret="abc123")

    def test_listen_with_secret_starts_server(self) -> None:
        client = Bavimail(api_key="bvm_test")

        @client.on(EventType.INBOUND_RECEIVED)
        def handler(event: WebhookEvent) -> None:
            pass

        mock_server_instance = MagicMock()
        mock_uvicorn = MagicMock()
        mock_uvicorn.Server.return_value = mock_server_instance

        import sys

        with patch.dict(sys.modules, {"uvicorn": mock_uvicorn}):
            client.listen(port=9999, secret=SECRET_HEX)

        mock_server_instance.run.assert_called_once()

    def test_listen_auto_create_and_cleanup(self) -> None:
        client = Bavimail(api_key="bvm_test")

        @client.on(EventType.INBOUND_RECEIVED)
        def handler(event: WebhookEvent) -> None:
            pass

        mock_webhook_created = MagicMock()
        mock_webhook_created.secret = SECRET_HEX
        mock_webhook_created.id = "wh-auto-123"

        client.webhooks.create = MagicMock(return_value=mock_webhook_created)  # type: ignore[assignment]
        client.webhooks.delete = MagicMock()  # type: ignore[assignment]

        mock_server_instance = MagicMock()
        mock_uvicorn = MagicMock()
        mock_uvicorn.Server.return_value = mock_server_instance

        import sys

        with patch.dict(sys.modules, {"uvicorn": mock_uvicorn}):
            client.listen(
                port=9999,
                webhook_url="https://example.com/webhooks",
            )

        client.webhooks.create.assert_called_once()
        client.webhooks.delete.assert_called_once_with("wh-auto-123")

    async def test_listen_async_no_handlers_raises(self) -> None:
        client = Bavimail(api_key="bvm_test")
        with pytest.raises(ValueError, match="No event handlers"):
            await client.listen_async(port=8080, secret="abc123")

    async def test_listen_async_no_url_or_secret_raises(self) -> None:
        client = Bavimail(api_key="bvm_test")

        @client.on(EventType.INBOUND_RECEIVED)
        def handler(event: WebhookEvent) -> None:
            pass

        with pytest.raises(ValueError, match="webhook_url.*secret"):
            await client.listen_async(port=8080)
