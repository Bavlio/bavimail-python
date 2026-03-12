"""Tests for HMAC authentication."""

from __future__ import annotations

import hashlib
import hmac
import time
from unittest.mock import patch

import httpx
import pytest

from bavimail._integration_auth import HMACAuth


class TestHMACAuth:
    """Tests for the HMACAuth class."""

    def test_build_canonical_string(self) -> None:
        """Test canonical string construction."""
        auth = HMACAuth("int_123", "abcd1234abcd1234abcd1234abcd1234")
        body = b'{"user_assertion": "user_token"}'
        timestamp = "1700000000"

        canonical = auth.build_canonical_string(
            method="POST",
            path="/integrations/int_123/api-keys/bootstrap",
            timestamp=timestamp,
            body=body,
        )

        expected_body_sha256 = hashlib.sha256(body).hexdigest()
        expected = (
            f"POST\n/integrations/int_123/api-keys/bootstrap\n{timestamp}\n{expected_body_sha256}"
        )
        assert canonical == expected

    def test_build_canonical_string_empty_body(self) -> None:
        """Test canonical string with empty body."""
        auth = HMACAuth("int_123", "abcd1234abcd1234abcd1234abcd1234")
        timestamp = "1700000000"

        canonical = auth.build_canonical_string(
            method="GET",
            path="/integrations",
            timestamp=timestamp,
            body=b"",
        )

        empty_sha256 = hashlib.sha256(b"").hexdigest()
        expected = f"GET\n/integrations\n{timestamp}\n{empty_sha256}"
        assert canonical == expected

    def test_build_canonical_string_with_query(self) -> None:
        """Test canonical string with query parameters."""
        auth = HMACAuth("int_123", "abcd1234abcd1234abcd1234abcd1234")
        timestamp = "1700000000"

        canonical = auth.build_canonical_string(
            method="GET",
            path="/integrations/int_123/webhooks?user_assertion=user_token",
            timestamp=timestamp,
            body=b"",
        )

        empty_sha256 = hashlib.sha256(b"").hexdigest()
        expected = (
            f"GET\n"
            f"/integrations/int_123/webhooks?user_assertion=user_token\n"
            f"{timestamp}\n"
            f"{empty_sha256}"
        )
        assert canonical == expected

    def test_compute_signature(self) -> None:
        """Test HMAC signature computation."""
        secret_hex = "abcd1234abcd1234abcd1234abcd1234"
        auth = HMACAuth("int_123", secret_hex)
        canonical = "POST\n/test\n1700000000\nabc123"

        signature = auth.compute_signature(canonical)

        expected = hmac.new(
            bytes.fromhex(secret_hex),
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        assert signature == expected

    def test_secret_as_bytes(self) -> None:
        """Test that secret can be provided as bytes."""
        secret_bytes = bytes.fromhex("abcd1234abcd1234abcd1234abcd1234")
        auth = HMACAuth("int_123", secret_bytes)
        canonical = "POST\n/test\n1700000000\nabc123"

        signature = auth.compute_signature(canonical)

        expected = hmac.new(
            secret_bytes,
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        assert signature == expected

    @patch("bavimail._integration_auth.time.time")
    def test_auth_flow_adds_headers(self, mock_time: patch) -> None:
        """Test that auth_flow adds correct headers to request."""
        mock_time.return_value = 1700000000
        secret_hex = "abcd1234abcd1234abcd1234abcd1234"
        auth = HMACAuth("int_123", secret_hex)

        body = b'{"user_assertion": "user_token"}'
        request = httpx.Request(
            "POST",
            "https://api.bavimail.com/integrations/int_123/api-keys/bootstrap",
            content=body,
        )

        # Run the auth flow
        flow = auth.auth_flow(request)
        signed_request = next(flow)

        # Check headers
        assert signed_request.headers["X-Timestamp"] == "1700000000"
        assert "X-Signature" in signed_request.headers

        # Verify the signature is correct
        body_sha256 = hashlib.sha256(body).hexdigest()
        canonical = f"POST\n/integrations/int_123/api-keys/bootstrap\n1700000000\n{body_sha256}"
        expected_signature = hmac.new(
            bytes.fromhex(secret_hex),
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        assert signed_request.headers["X-Signature"] == expected_signature

    @patch("bavimail._integration_auth.time.time")
    def test_auth_flow_with_query_params(self, mock_time: patch) -> None:
        """Test that auth_flow excludes query params from canonical string."""
        mock_time.return_value = 1700000000
        secret_hex = "abcd1234abcd1234abcd1234abcd1234"
        auth = HMACAuth("int_123", secret_hex)

        request = httpx.Request(
            "GET",
            "https://api.bavimail.com/integrations/int_123/webhooks",
            params={"user_assertion": "user_token"},
        )

        flow = auth.auth_flow(request)
        signed_request = next(flow)

        # Verify the signature excludes query params
        empty_sha256 = hashlib.sha256(b"").hexdigest()
        canonical = f"GET\n/integrations/int_123/webhooks\n1700000000\n{empty_sha256}"
        expected_signature = hmac.new(
            bytes.fromhex(secret_hex),
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        assert signed_request.headers["X-Signature"] == expected_signature

    def test_auth_flow_uses_current_time(self) -> None:
        """Test that auth_flow uses current Unix timestamp."""
        auth = HMACAuth("int_123", "abcd1234abcd1234abcd1234abcd1234")

        request = httpx.Request("GET", "https://api.bavimail.com/integrations")

        before = int(time.time())
        flow = auth.auth_flow(request)
        signed_request = next(flow)
        after = int(time.time())

        timestamp = int(signed_request.headers["X-Timestamp"])
        assert before <= timestamp <= after
