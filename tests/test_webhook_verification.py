"""Tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac
import time

import pytest

from bavimail.exceptions import WebhookVerificationError
from bavimail.webhook_verification import verify_webhook_signature

SECRET_HEX = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
PAYLOAD = '{"event": "test"}'


def _compute_signature(secret: str, timestamp: str, body: str) -> str:
    """Mirror the server-side signature computation."""
    signing_string = f"{timestamp}.{body}"
    return hmac.new(
        bytes.fromhex(secret),
        signing_string.encode(),
        hashlib.sha256,
    ).hexdigest()


def test_valid_signature() -> None:
    ts = str(int(time.time()))
    sig = _compute_signature(SECRET_HEX, ts, PAYLOAD)
    verify_webhook_signature(
        payload=PAYLOAD,
        signature=sig,
        timestamp=ts,
        secret=SECRET_HEX,
    )


def test_valid_signature_with_prefix() -> None:
    ts = str(int(time.time()))
    sig = _compute_signature(SECRET_HEX, ts, PAYLOAD)
    verify_webhook_signature(
        payload=PAYLOAD,
        signature=f"sha256={sig}",
        timestamp=ts,
        secret=SECRET_HEX,
    )


def test_valid_signature_bytes_payload() -> None:
    ts = str(int(time.time()))
    sig = _compute_signature(SECRET_HEX, ts, PAYLOAD)
    verify_webhook_signature(
        payload=PAYLOAD.encode(),
        signature=sig,
        timestamp=ts,
        secret=SECRET_HEX,
    )


def test_invalid_signature() -> None:
    ts = str(int(time.time()))
    with pytest.raises(WebhookVerificationError, match="Signature mismatch"):
        verify_webhook_signature(
            payload=PAYLOAD,
            signature="invalid",
            timestamp=ts,
            secret=SECRET_HEX,
        )


def test_expired_timestamp() -> None:
    ts = str(int(time.time()) - 600)  # 10 minutes ago
    sig = _compute_signature(SECRET_HEX, ts, PAYLOAD)
    with pytest.raises(WebhookVerificationError, match="too old"):
        verify_webhook_signature(
            payload=PAYLOAD,
            signature=sig,
            timestamp=ts,
            secret=SECRET_HEX,
            tolerance=300,
        )


def test_tolerance_none_skips_time_check() -> None:
    ts = str(int(time.time()) - 99999)
    sig = _compute_signature(SECRET_HEX, ts, PAYLOAD)
    verify_webhook_signature(
        payload=PAYLOAD,
        signature=sig,
        timestamp=ts,
        secret=SECRET_HEX,
        tolerance=None,
    )


def test_invalid_timestamp_format() -> None:
    sig = _compute_signature(SECRET_HEX, "not-a-number", PAYLOAD)
    with pytest.raises(WebhookVerificationError, match="Invalid timestamp"):
        verify_webhook_signature(
            payload=PAYLOAD,
            signature=sig,
            timestamp="not-a-number",
            secret=SECRET_HEX,
        )
