"""Tests for the Flask webhook blueprint integration."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

import pytest

from bavimail.events import EventType, WebhookEvent
from bavimail.integrations.flask import create_webhook_blueprint

SECRET_HEX = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

SAMPLE_EVENT = {
    "event_id": "evt-flask-001",
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
def flask_app() -> Any:
    flask = pytest.importorskip("flask")
    app = flask.Flask(__name__)
    results: list[str] = []

    def handler(event: WebhookEvent) -> None:
        results.append(event.event_id)

    bp = create_webhook_blueprint(
        handlers={EventType.INBOUND_RECEIVED: [handler]},
        secret=SECRET_HEX,
        path="/webhooks",
    )
    app.register_blueprint(bp)
    app.config["results"] = results
    return app


def test_health_check(flask_app: Any) -> None:
    with flask_app.test_client() as client:
        resp = client.get("/webhooks")
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "ok"}


def test_valid_webhook(flask_app: Any) -> None:
    body = json.dumps(SAMPLE_EVENT).encode()
    sig, ts = _sign(body)
    with flask_app.test_client() as client:
        resp = client.post(
            "/webhooks",
            data=body,
            content_type="application/json",
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
            },
        )
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "ok"}
    assert flask_app.config["results"] == ["evt-flask-001"]


def test_invalid_signature(flask_app: Any) -> None:
    body = json.dumps(SAMPLE_EVENT).encode()
    with flask_app.test_client() as client:
        resp = client.post(
            "/webhooks",
            data=body,
            content_type="application/json",
            headers={
                "x-webhook-signature": "bad",
                "x-webhook-timestamp": str(int(time.time())),
            },
        )
        assert resp.status_code == 403


def test_invalid_json(flask_app: Any) -> None:
    body = b"not json"
    sig, ts = _sign(body)
    with flask_app.test_client() as client:
        resp = client.post(
            "/webhooks",
            data=body,
            content_type="application/json",
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
            },
        )
        assert resp.status_code == 400


def test_handler_error_still_returns_200(flask_app: Any) -> None:
    """Add a handler that raises; the blueprint should still return 200."""
    flask = pytest.importorskip("flask")
    app = flask.Flask(__name__)

    def bad_handler(event: WebhookEvent) -> None:
        raise RuntimeError("boom")

    bp = create_webhook_blueprint(
        handlers={EventType.INBOUND_RECEIVED: [bad_handler]},
        secret=SECRET_HEX,
        path="/webhooks",
    )
    app.register_blueprint(bp)

    body = json.dumps(SAMPLE_EVENT).encode()
    sig, ts = _sign(body)
    with app.test_client() as client:
        resp = client.post(
            "/webhooks",
            data=body,
            content_type="application/json",
            headers={
                "x-webhook-signature": sig,
                "x-webhook-timestamp": ts,
            },
        )
        assert resp.status_code == 200
