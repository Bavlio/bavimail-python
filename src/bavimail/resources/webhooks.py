"""Webhooks resource."""

from __future__ import annotations

from typing import Any

from .._types import UNSET, _UnsetType
from ..models.webhook import Webhook, WebhookCreated, WebhookSecret
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Webhooks(BaseResource):
    """Operations on webhooks."""

    def create(
        self,
        url: str,
        event_types: _List[str],
        *,
        description: str | None = None,
    ) -> WebhookCreated:
        """Create a new webhook. Returns the secret (shown once)."""
        body: dict[str, Any] = {"url": url, "event_types": event_types}
        if description is not None:
            body["description"] = description
        data = self._http.request("POST", "/webhooks", json=body)
        return WebhookCreated.from_dict(data)

    async def create_async(
        self,
        url: str,
        event_types: _List[str],
        *,
        description: str | None = None,
    ) -> WebhookCreated:
        """Create a new webhook (async). Returns the secret (shown once)."""
        body: dict[str, Any] = {"url": url, "event_types": event_types}
        if description is not None:
            body["description"] = description
        data = await self._http.request_async("POST", "/webhooks", json=body)
        return WebhookCreated.from_dict(data)

    def list(self) -> _List[Webhook]:
        """List all webhooks."""
        data = self._http.request("GET", "/webhooks")
        return [Webhook.from_dict(w) for w in data]

    async def list_async(self) -> _List[Webhook]:
        """List all webhooks (async)."""
        data = await self._http.request_async("GET", "/webhooks")
        return [Webhook.from_dict(w) for w in data]

    def get(self, webhook_id: str) -> Webhook:
        """Get a webhook by ID."""
        data = self._http.request("GET", f"/webhooks/{webhook_id}")
        return Webhook.from_dict(data)

    async def get_async(self, webhook_id: str) -> Webhook:
        """Get a webhook by ID (async)."""
        data = await self._http.request_async("GET", f"/webhooks/{webhook_id}")
        return Webhook.from_dict(data)

    def update(
        self,
        webhook_id: str,
        *,
        url: str | _UnsetType = UNSET,
        event_types: _List[str] | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
        is_active: bool | _UnsetType = UNSET,
    ) -> Webhook:
        """Update a webhook."""
        body: dict[str, Any] = {}
        if url is not UNSET:
            body["url"] = url
        if event_types is not UNSET:
            body["event_types"] = event_types
        if description is not UNSET:
            body["description"] = description
        if is_active is not UNSET:
            body["is_active"] = is_active
        data = self._http.request("PATCH", f"/webhooks/{webhook_id}", json=body)
        return Webhook.from_dict(data)

    async def update_async(
        self,
        webhook_id: str,
        *,
        url: str | _UnsetType = UNSET,
        event_types: _List[str] | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
        is_active: bool | _UnsetType = UNSET,
    ) -> Webhook:
        """Update a webhook (async)."""
        body: dict[str, Any] = {}
        if url is not UNSET:
            body["url"] = url
        if event_types is not UNSET:
            body["event_types"] = event_types
        if description is not UNSET:
            body["description"] = description
        if is_active is not UNSET:
            body["is_active"] = is_active
        data = await self._http.request_async(
            "PATCH", f"/webhooks/{webhook_id}", json=body
        )
        return Webhook.from_dict(data)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook."""
        self._http.request("DELETE", f"/webhooks/{webhook_id}")

    async def delete_async(self, webhook_id: str) -> None:
        """Delete a webhook (async)."""
        await self._http.request_async("DELETE", f"/webhooks/{webhook_id}")

    def verify(self, webhook_id: str, verification_code: str) -> Webhook:
        """Submit a verification code."""
        data = self._http.request(
            "POST",
            f"/webhooks/{webhook_id}/verify",
            json={"verification_code": verification_code},
        )
        return Webhook.from_dict(data)

    async def verify_async(
        self, webhook_id: str, verification_code: str
    ) -> Webhook:
        """Submit a verification code (async)."""
        data = await self._http.request_async(
            "POST",
            f"/webhooks/{webhook_id}/verify",
            json={"verification_code": verification_code},
        )
        return Webhook.from_dict(data)

    def resend_verification(self, webhook_id: str) -> Webhook:
        """Resend verification code to the webhook URL."""
        data = self._http.request(
            "POST", f"/webhooks/{webhook_id}/resend-verification"
        )
        return Webhook.from_dict(data)

    async def resend_verification_async(self, webhook_id: str) -> Webhook:
        """Resend verification code to the webhook URL (async)."""
        data = await self._http.request_async(
            "POST", f"/webhooks/{webhook_id}/resend-verification"
        )
        return Webhook.from_dict(data)

    def test(self, webhook_id: str) -> dict[str, str]:
        """Send a test event to a verified, active webhook."""
        data = self._http.request(
            "POST", f"/webhooks/{webhook_id}/test"
        )
        return data  # type: ignore[no-any-return]

    async def test_async(self, webhook_id: str) -> dict[str, str]:
        """Send a test event to a verified, active webhook (async)."""
        data = await self._http.request_async(
            "POST", f"/webhooks/{webhook_id}/test"
        )
        return data  # type: ignore[no-any-return]

    def rotate_secret(self, webhook_id: str) -> WebhookSecret:
        """Rotate the HMAC signing secret."""
        data = self._http.request(
            "POST", f"/webhooks/{webhook_id}/rotate-secret"
        )
        return WebhookSecret.from_dict(data)

    async def rotate_secret_async(self, webhook_id: str) -> WebhookSecret:
        """Rotate the HMAC signing secret (async)."""
        data = await self._http.request_async(
            "POST", f"/webhooks/{webhook_id}/rotate-secret"
        )
        return WebhookSecret.from_dict(data)
