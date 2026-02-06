"""Webhook signature verification utility."""

from __future__ import annotations

import hashlib
import hmac
import time

from .exceptions import WebhookVerificationError

DEFAULT_TOLERANCE_SECONDS = 300  # 5 minutes


def verify_webhook_signature(
    *,
    payload: str | bytes,
    signature: str,
    timestamp: str,
    secret: str,
    tolerance: int | None = DEFAULT_TOLERANCE_SECONDS,
) -> None:
    """Verify a Bavimail webhook signature.

    Mirrors the server-side algorithm in ``app/services/webhooks/signer.py``:
    HMAC-SHA256 of ``"{timestamp}.{body}"`` using the hex-decoded secret.

    Args:
        payload: The raw request body (string or bytes).
        signature: The ``x-webhook-signature`` header value.
            May include a ``sha256=`` prefix.
        timestamp: The ``x-webhook-timestamp`` header value (Unix epoch string).
        secret: The hex-encoded HMAC secret for this webhook.
        tolerance: Maximum age in seconds (default 300). Set to ``None``
            to skip timestamp checking.

    Raises:
        WebhookVerificationError: If the signature is invalid or the
            timestamp is too old.
    """
    # Strip optional prefix
    if signature.startswith("sha256="):
        signature = signature[7:]

    # Validate timestamp freshness
    if tolerance is not None:
        try:
            ts = int(timestamp)
        except (ValueError, TypeError) as exc:
            raise WebhookVerificationError("Invalid timestamp format") from exc
        age = abs(int(time.time()) - ts)
        if age > tolerance:
            raise WebhookVerificationError(
                f"Timestamp too old ({age}s > {tolerance}s tolerance)"
            )

    # Compute expected signature
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    signing_string = f"{timestamp}.{payload}"
    expected = hmac.new(
        bytes.fromhex(secret),
        signing_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison
    if not hmac.compare_digest(expected, signature):
        raise WebhookVerificationError("Signature mismatch")
