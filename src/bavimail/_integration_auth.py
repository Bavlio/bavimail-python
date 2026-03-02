"""HMAC authentication for integration client."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Generator

import httpx


class HMACAuth(httpx.Auth):
    """HMAC-SHA256 authentication for integration API requests.

    Signs requests using:
    - X-Timestamp: Unix epoch timestamp
    - X-Signature: HMAC-SHA256 signature of canonical request string

    Canonical string format:
        {METHOD}\\n{PATH}\\n{TIMESTAMP}\\n{BODY_SHA256}

    Where BODY_SHA256 is the SHA-256 hex digest of the raw request body.

    Note: the signed PATH excludes query parameters to match Bavimail
    server-side verification.
    """

    def __init__(self, integration_id: str, secret: str | bytes) -> None:
        """Initialize HMAC auth.

        Args:
            integration_id: The integration ID (used for reference, not signing).
            secret: The hex-encoded secret key for HMAC signing.
        """
        self.integration_id = integration_id
        if isinstance(secret, str):
            self._secret = bytes.fromhex(secret)
        else:
            self._secret = secret

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Add HMAC signature headers to the request."""
        timestamp = str(int(time.time()))
        body = request.content or b""
        body_sha256 = hashlib.sha256(body).hexdigest()

        # Build canonical string
        path = request.url.path
        canonical = f"{request.method}\n{path}\n{timestamp}\n{body_sha256}"

        # Compute HMAC signature
        signature = hmac.new(self._secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()

        # Add headers
        request.headers["X-Timestamp"] = timestamp
        request.headers["X-Signature"] = signature

        yield request

    def build_canonical_string(self, method: str, path: str, timestamp: str, body: bytes) -> str:
        """Build the canonical string for signing (exposed for testing).

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path used in canonical signing
            timestamp: Unix epoch timestamp as string
            body: Raw request body bytes

        Returns:
            The canonical string to be signed.
        """
        body_sha256 = hashlib.sha256(body).hexdigest()
        return f"{method}\n{path}\n{timestamp}\n{body_sha256}"

    def compute_signature(self, canonical_string: str) -> str:
        """Compute the HMAC-SHA256 signature (exposed for testing).

        Args:
            canonical_string: The canonical request string.

        Returns:
            Hex-encoded HMAC-SHA256 signature.
        """
        return hmac.new(self._secret, canonical_string.encode("utf-8"), hashlib.sha256).hexdigest()
