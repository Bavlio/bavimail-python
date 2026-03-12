"""Integration client for B2B service-level operations using HMAC auth."""

from __future__ import annotations

from types import TracebackType
from typing import Any

import httpx

from ._integration_auth import HMACAuth
from ._version import __version__
from .exceptions import _raise_for_status
from .models.integration import (
    BootstrapApiKeyResponse,
    IntegrationInfo,
    RevokeApiKeyResponse,
)
from .models.webhook import Webhook, WebhookCreated


class IntegrationClient:
    """Client for B2B integration operations using HMAC authentication.

    This client is separate from the main Bavimail client because it uses
    a different authentication mechanism (HMAC vs API key) and is designed
    for service-level B2B integrations.

    Example::

        client = IntegrationClient(
            integration_id="int_abc123",
            integration_secret="hex_secret",
        )

        # Bootstrap API key for a user
        result = client.bootstrap_api_key("user_assertion_jwt")
        print(f"API Key: {result.api_key}")

    Args:
        integration_id: Your integration ID.
        integration_secret: Hex-encoded HMAC secret for signing requests.
        base_url: Base URL of the Bavimail API (default ``https://api.bavimail.com``).
        timeout: Request timeout in seconds (default 30).
        http_client: Optional custom ``httpx.Client`` for sync requests.
        async_http_client: Optional custom ``httpx.AsyncClient`` for async requests.
    """

    def __init__(
        self,
        *,
        integration_id: str,
        integration_secret: str,
        base_url: str = "https://api.bavimail.com",
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
        async_http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self._base_url = base_url
        self._integration_id = integration_id
        self._auth = HMACAuth(integration_id, integration_secret)
        self._timeout = timeout
        self._custom_client = http_client
        self._custom_async_client = async_http_client
        self._client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    @property
    def _default_headers(self) -> dict[str, str]:
        return {
            "User-Agent": f"bavimail-python/{__version__}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _get_client(self) -> httpx.Client:
        if self._custom_client is not None:
            return self._custom_client
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                headers=self._default_headers,
                timeout=self._timeout,
                auth=self._auth,
            )
        return self._client

    def _get_async_client(self) -> httpx.AsyncClient:
        if self._custom_async_client is not None:
            return self._custom_async_client
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                headers=self._default_headers,
                timeout=self._timeout,
                auth=self._auth,
            )
        return self._async_client

    def _build_path(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return path

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make a synchronous HTTP request."""
        client = self._get_client()
        url = self._build_path(path)
        # Clean None values from params
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
        response = client.request(method, url, json=json, params=params)
        request_id = response.headers.get("x-request-id")
        if response.status_code == 204:
            return None
        body = response.json() if response.content else None
        _raise_for_status(response.status_code, body, request_id)
        return body

    async def _request_async(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make an asynchronous HTTP request."""
        client = self._get_async_client()
        url = self._build_path(path)
        # Clean None values from params
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
        response = await client.request(method, url, json=json, params=params)
        request_id = response.headers.get("x-request-id")
        if response.status_code == 204:
            return None
        body = response.json() if response.content else None
        _raise_for_status(response.status_code, body, request_id)
        return body

    # -- Static methods (no auth) ----------------------------------------------

    @classmethod
    def list_integrations(
        cls,
        base_url: str = "https://api.bavimail.com",
        timeout: float = 30.0,
    ) -> list[IntegrationInfo]:
        """List available integrations (no authentication required).

        Args:
            base_url: Base URL of the Bavimail API.
            timeout: Request timeout in seconds.

        Returns:
            List of available integrations.
        """
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        with httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "User-Agent": f"bavimail-python/{__version__}",
                "Accept": "application/json",
            },
        ) as client:
            response = client.get("/integrations")
            request_id = response.headers.get("x-request-id")
            body = response.json() if response.content else None
            _raise_for_status(response.status_code, body, request_id)
            return [IntegrationInfo.from_dict(item) for item in body]

    @classmethod
    async def list_integrations_async(
        cls,
        base_url: str = "https://api.bavimail.com",
        timeout: float = 30.0,
    ) -> list[IntegrationInfo]:
        """List available integrations (async, no authentication required).

        Args:
            base_url: Base URL of the Bavimail API.
            timeout: Request timeout in seconds.

        Returns:
            List of available integrations.
        """
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        async with httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "User-Agent": f"bavimail-python/{__version__}",
                "Accept": "application/json",
            },
        ) as client:
            response = await client.get("/integrations")
            request_id = response.headers.get("x-request-id")
            body = response.json() if response.content else None
            _raise_for_status(response.status_code, body, request_id)
            return [IntegrationInfo.from_dict(item) for item in body]

    # -- API Key operations ----------------------------------------------------

    def bootstrap_api_key(
        self,
        user_assertion: str,
        *,
        label: str | None = None,
    ) -> BootstrapApiKeyResponse:
        """Bootstrap an API key for a user.

        Creates a new API key for the user identified by the signed user assertion,
        or returns an existing key if one already exists.

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            label: Optional label for the API key.

        Returns:
            Bootstrap response containing the API key.
        """
        path = f"/integrations/{self._integration_id}/api-keys/bootstrap"
        payload: dict[str, Any] = {"user_assertion": user_assertion}
        if label is not None:
            payload["label"] = label
        data = self._request("POST", path, json=payload)
        return BootstrapApiKeyResponse.from_dict(data)

    async def bootstrap_api_key_async(
        self,
        user_assertion: str,
        *,
        label: str | None = None,
    ) -> BootstrapApiKeyResponse:
        """Bootstrap an API key for a user (async).

        Creates a new API key for the user identified by the signed user assertion,
        or returns an existing key if one already exists.

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            label: Optional label for the API key.

        Returns:
            Bootstrap response containing the API key.
        """
        path = f"/integrations/{self._integration_id}/api-keys/bootstrap"
        payload: dict[str, Any] = {"user_assertion": user_assertion}
        if label is not None:
            payload["label"] = label
        data = await self._request_async("POST", path, json=payload)
        return BootstrapApiKeyResponse.from_dict(data)

    def revoke_api_key(self, user_assertion: str) -> RevokeApiKeyResponse:
        """Revoke an API key for a user.

        Args:
            user_assertion: Signed JWT assertion identifying the user.

        Returns:
            Revoke response indicating success.
        """
        path = f"/integrations/{self._integration_id}/api-key"
        payload = {"user_assertion": user_assertion}
        data = self._request("DELETE", path, json=payload)
        return RevokeApiKeyResponse.from_dict(data)

    async def revoke_api_key_async(self, user_assertion: str) -> RevokeApiKeyResponse:
        """Revoke an API key for a user (async).

        Args:
            user_assertion: Signed JWT assertion identifying the user.

        Returns:
            Revoke response indicating success.
        """
        path = f"/integrations/{self._integration_id}/api-key"
        payload = {"user_assertion": user_assertion}
        data = await self._request_async("DELETE", path, json=payload)
        return RevokeApiKeyResponse.from_dict(data)

    # -- Webhook operations ----------------------------------------------------

    def create_webhook(
        self,
        user_assertion: str,
        url: str,
        event_types: list[str],
        *,
        description: str | None = None,
        secret: str | None = None,
    ) -> WebhookCreated:
        """Create a webhook for a user.

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            url: HTTPS URL where webhook events will be delivered.
            event_types: List of event types to subscribe to.
            description: Optional description for the webhook.
            secret: Optional hex-encoded secret (64-128 chars). If omitted,
                a random secret is generated. Pass the integration secret
                to use a shared secret for all webhooks.

        Returns:
            Created webhook including the secret.
        """
        path = f"/integrations/{self._integration_id}/webhooks"
        payload: dict[str, Any] = {
            "user_assertion": user_assertion,
            "url": url,
            "event_types": event_types,
        }
        if description is not None:
            payload["description"] = description
        if secret is not None:
            payload["secret"] = secret
        data = self._request("POST", path, json=payload)
        return WebhookCreated.from_dict(data)

    async def create_webhook_async(
        self,
        user_assertion: str,
        url: str,
        event_types: list[str],
        *,
        description: str | None = None,
        secret: str | None = None,
    ) -> WebhookCreated:
        """Create a webhook for a user (async).

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            url: HTTPS URL where webhook events will be delivered.
            event_types: List of event types to subscribe to.
            description: Optional description for the webhook.
            secret: Optional hex-encoded secret (64-128 chars). If omitted,
                a random secret is generated. Pass the integration secret
                to use a shared secret for all webhooks.

        Returns:
            Created webhook including the secret.
        """
        path = f"/integrations/{self._integration_id}/webhooks"
        payload: dict[str, Any] = {
            "user_assertion": user_assertion,
            "url": url,
            "event_types": event_types,
        }
        if description is not None:
            payload["description"] = description
        if secret is not None:
            payload["secret"] = secret
        data = await self._request_async("POST", path, json=payload)
        return WebhookCreated.from_dict(data)

    def list_webhooks(self, user_assertion: str) -> list[Webhook]:
        """List webhooks for a user.

        Args:
            user_assertion: Signed JWT assertion identifying the user.

        Returns:
            List of webhooks for the user.
        """
        path = f"/integrations/{self._integration_id}/webhooks"
        params = {"user_assertion": user_assertion}
        data = self._request("GET", path, params=params)
        return [Webhook.from_dict(item) for item in data]

    async def list_webhooks_async(self, user_assertion: str) -> list[Webhook]:
        """List webhooks for a user (async).

        Args:
            user_assertion: Signed JWT assertion identifying the user.

        Returns:
            List of webhooks for the user.
        """
        path = f"/integrations/{self._integration_id}/webhooks"
        params = {"user_assertion": user_assertion}
        data = await self._request_async("GET", path, params=params)
        return [Webhook.from_dict(item) for item in data]

    def delete_webhook(self, user_assertion: str, webhook_id: str) -> None:
        """Delete a webhook.

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            webhook_id: ID of the webhook to delete.
        """
        path = f"/integrations/{self._integration_id}/webhooks/{webhook_id}"
        payload = {"user_assertion": user_assertion}
        self._request("DELETE", path, json=payload)

    async def delete_webhook_async(self, user_assertion: str, webhook_id: str) -> None:
        """Delete a webhook (async).

        Args:
            user_assertion: Signed JWT assertion identifying the user.
            webhook_id: ID of the webhook to delete.
        """
        path = f"/integrations/{self._integration_id}/webhooks/{webhook_id}"
        payload = {"user_assertion": user_assertion}
        await self._request_async("DELETE", path, json=payload)

    # -- Lifecycle -------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client(s)."""
        if self._client is not None:
            self._client.close()
            self._client = None

    async def aclose(self) -> None:
        """Close the underlying async HTTP client."""
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def __enter__(self) -> IntegrationClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> IntegrationClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()
