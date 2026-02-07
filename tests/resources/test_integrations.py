"""Tests for IntegrationClient."""

from __future__ import annotations

from typing import Any, Callable
from unittest.mock import patch

import httpx
import pytest

from bavimail import IntegrationClient
from bavimail._integration_auth import HMACAuth
from bavimail.models import BootstrapApiKeyResponse, IntegrationInfo, RevokeApiKeyResponse
from bavimail.models.webhook import Webhook, WebhookCreated

from tests.conftest import (
    SAMPLE_BOOTSTRAP_RESPONSE,
    SAMPLE_INTEGRATION,
    SAMPLE_REVOKE_RESPONSE,
    SAMPLE_WEBHOOK,
    SAMPLE_WEBHOOK_CREATED,
    json_response,
    make_mock_transport,
    no_content_response,
)

INTEGRATION_ID = "int_001"
INTEGRATION_SECRET = "abcd1234abcd1234abcd1234abcd1234"


def make_integration_client(
    base_url: str,
    handler: Callable[[httpx.Request], httpx.Response],
) -> IntegrationClient:
    """Create an IntegrationClient with a mock transport."""
    transport = make_mock_transport(handler)
    auth = HMACAuth(INTEGRATION_ID, INTEGRATION_SECRET)
    sync_client = httpx.Client(transport=transport, base_url=base_url, auth=auth)
    return IntegrationClient(
        integration_id=INTEGRATION_ID,
        integration_secret=INTEGRATION_SECRET,
        base_url=base_url,
        http_client=sync_client,
    )


def make_async_integration_client(
    base_url: str,
    handler: Callable[[httpx.Request], httpx.Response],
) -> IntegrationClient:
    """Create an IntegrationClient with an async mock transport."""
    transport = make_mock_transport(handler)
    auth = HMACAuth(INTEGRATION_ID, INTEGRATION_SECRET)
    async_client = httpx.AsyncClient(transport=transport, base_url=base_url, auth=auth)
    return IntegrationClient(
        integration_id=INTEGRATION_ID,
        integration_secret=INTEGRATION_SECRET,
        base_url=base_url,
        async_http_client=async_client,
    )


class TestListIntegrations:
    """Tests for list_integrations class method."""

    def test_list_integrations(self) -> None:
        """Test listing integrations without authentication."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/integrations"
            assert request.method == "GET"
            # Should not have X-Signature header (no auth)
            return json_response([SAMPLE_INTEGRATION])

        transport = make_mock_transport(handler)

        # Patch httpx.Client to use our mock transport
        original_client = httpx.Client

        def patched_client(*args: Any, **kwargs: Any) -> httpx.Client:
            kwargs["transport"] = transport
            return original_client(*args, **kwargs)

        with patch("httpx.Client", side_effect=patched_client):
            result = IntegrationClient.list_integrations(base_url=base_url)

        assert len(result) == 1
        assert isinstance(result[0], IntegrationInfo)
        assert result[0].id == "int_001"
        assert result[0].display_name == "Test Integration"
        assert result[0].auth_mode == "hmac"

    @pytest.mark.asyncio
    async def test_list_integrations_async(self) -> None:
        """Test listing integrations async without authentication."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/integrations"
            return json_response([SAMPLE_INTEGRATION])

        transport = make_mock_transport(handler)

        # Patch httpx.AsyncClient to use our mock transport
        original_client = httpx.AsyncClient

        def patched_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
            kwargs["transport"] = transport
            return original_client(*args, **kwargs)

        with patch("httpx.AsyncClient", side_effect=patched_client):
            result = await IntegrationClient.list_integrations_async(base_url=base_url)

        assert len(result) == 1
        assert isinstance(result[0], IntegrationInfo)


class TestBootstrapApiKey:
    """Tests for bootstrap_api_key."""

    def test_bootstrap_api_key(self) -> None:
        """Test bootstrapping an API key."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/integrations/int_001/api-keys/bootstrap"
            assert request.method == "POST"
            # Check HMAC headers are present
            assert "X-Timestamp" in request.headers
            assert "X-Signature" in request.headers
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_integration_client(base_url, handler)
        result = client.bootstrap_api_key("user_token_123")

        assert isinstance(result, BootstrapApiKeyResponse)
        assert result.api_key == "bvm_test_bootstrapped_key_12345"
        assert result.created is True
        assert result.expires_at is None

    def test_bootstrap_api_key_with_label(self) -> None:
        """Test bootstrapping an API key with label."""
        base_url = "https://api.bavimail.test"
        captured_body: dict[str, Any] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            import json
            captured_body.update(json.loads(request.content))
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_integration_client(base_url, handler)
        client.bootstrap_api_key("user_token_123", label="Production Key")

        assert captured_body["external_token"] == "user_token_123"
        assert captured_body["label"] == "Production Key"

    @pytest.mark.asyncio
    async def test_bootstrap_api_key_async(self) -> None:
        """Test bootstrapping an API key async."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_async_integration_client(base_url, handler)
        result = await client.bootstrap_api_key_async("user_token_123")

        assert isinstance(result, BootstrapApiKeyResponse)
        assert result.api_key == "bvm_test_bootstrapped_key_12345"


class TestRevokeApiKey:
    """Tests for revoke_api_key."""

    def test_revoke_api_key(self) -> None:
        """Test revoking an API key."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/integrations/int_001/api-key"
            assert request.method == "DELETE"
            assert "X-Signature" in request.headers
            return json_response(SAMPLE_REVOKE_RESPONSE)

        client = make_integration_client(base_url, handler)
        result = client.revoke_api_key("user_token_123")

        assert isinstance(result, RevokeApiKeyResponse)
        assert result.revoked is True

    @pytest.mark.asyncio
    async def test_revoke_api_key_async(self) -> None:
        """Test revoking an API key async."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_REVOKE_RESPONSE)

        client = make_async_integration_client(base_url, handler)
        result = await client.revoke_api_key_async("user_token_123")

        assert isinstance(result, RevokeApiKeyResponse)
        assert result.revoked is True


class TestCreateWebhook:
    """Tests for create_webhook."""

    def test_create_webhook(self) -> None:
        """Test creating a webhook."""
        base_url = "https://api.bavimail.test"
        captured_body: dict[str, Any] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            import json
            assert request.url.path == "/integrations/int_001/webhooks"
            assert request.method == "POST"
            captured_body.update(json.loads(request.content))
            return json_response(SAMPLE_WEBHOOK_CREATED)

        client = make_integration_client(base_url, handler)
        result = client.create_webhook(
            external_token="user_token_123",
            url="https://example.com/webhook",
            event_types=["email.inbound.received"],
            description="Test webhook",
        )

        assert isinstance(result, WebhookCreated)
        assert result.secret == "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        assert captured_body["external_token"] == "user_token_123"
        assert captured_body["url"] == "https://example.com/webhook"
        assert captured_body["event_types"] == ["email.inbound.received"]
        assert captured_body["description"] == "Test webhook"

    @pytest.mark.asyncio
    async def test_create_webhook_async(self) -> None:
        """Test creating a webhook async."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_WEBHOOK_CREATED)

        client = make_async_integration_client(base_url, handler)
        result = await client.create_webhook_async(
            external_token="user_token_123",
            url="https://example.com/webhook",
            event_types=["email.inbound.received"],
        )

        assert isinstance(result, WebhookCreated)


class TestListWebhooks:
    """Tests for list_webhooks."""

    def test_list_webhooks(self) -> None:
        """Test listing webhooks."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/integrations/int_001/webhooks"
            assert request.method == "GET"
            assert "external_token=user_token_123" in str(request.url)
            return json_response([SAMPLE_WEBHOOK])

        client = make_integration_client(base_url, handler)
        result = client.list_webhooks("user_token_123")

        assert len(result) == 1
        assert isinstance(result[0], Webhook)
        assert result[0].id == "w1000000-0000-0000-0000-000000000001"

    @pytest.mark.asyncio
    async def test_list_webhooks_async(self) -> None:
        """Test listing webhooks async."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response([SAMPLE_WEBHOOK])

        client = make_async_integration_client(base_url, handler)
        result = await client.list_webhooks_async("user_token_123")

        assert len(result) == 1
        assert isinstance(result[0], Webhook)


class TestDeleteWebhook:
    """Tests for delete_webhook."""

    def test_delete_webhook(self) -> None:
        """Test deleting a webhook."""
        base_url = "https://api.bavimail.test"
        captured_body: dict[str, Any] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            import json
            assert "/integrations/int_001/webhooks/wh_123" in request.url.path
            assert request.method == "DELETE"
            captured_body.update(json.loads(request.content))
            return no_content_response()

        client = make_integration_client(base_url, handler)
        client.delete_webhook("user_token_123", "wh_123")

        assert captured_body["external_token"] == "user_token_123"

    @pytest.mark.asyncio
    async def test_delete_webhook_async(self) -> None:
        """Test deleting a webhook async."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return no_content_response()

        client = make_async_integration_client(base_url, handler)
        await client.delete_webhook_async("user_token_123", "wh_123")


class TestClientLifecycle:
    """Tests for client lifecycle management."""

    def test_context_manager(self) -> None:
        """Test sync context manager."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        with make_integration_client(base_url, handler) as client:
            result = client.bootstrap_api_key("user_token")
            assert result.api_key == "bvm_test_bootstrapped_key_12345"

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        """Test async context manager."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        async with make_async_integration_client(base_url, handler) as client:
            result = await client.bootstrap_api_key_async("user_token")
            assert result.api_key == "bvm_test_bootstrapped_key_12345"

    def test_close(self) -> None:
        """Test explicit close."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_integration_client(base_url, handler)
        client.bootstrap_api_key("user_token")
        client.close()

    @pytest.mark.asyncio
    async def test_aclose(self) -> None:
        """Test explicit aclose."""
        base_url = "https://api.bavimail.test"

        def handler(request: httpx.Request) -> httpx.Response:
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_async_integration_client(base_url, handler)
        await client.bootstrap_api_key_async("user_token")
        await client.aclose()


class TestHMACHeaders:
    """Tests for HMAC authentication headers."""

    def test_hmac_headers_present(self) -> None:
        """Test that HMAC headers are added to requests."""
        base_url = "https://api.bavimail.test"
        captured_headers: dict[str, str] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured_headers["X-Timestamp"] = request.headers.get("X-Timestamp", "")
            captured_headers["X-Signature"] = request.headers.get("X-Signature", "")
            return json_response(SAMPLE_BOOTSTRAP_RESPONSE)

        client = make_integration_client(base_url, handler)
        client.bootstrap_api_key("user_token")

        assert captured_headers["X-Timestamp"] != ""
        assert captured_headers["X-Signature"] != ""
        # Timestamp should be a valid integer
        int(captured_headers["X-Timestamp"])
        # Signature should be a hex string (64 chars for SHA256)
        assert len(captured_headers["X-Signature"]) == 64
