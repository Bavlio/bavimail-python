"""Webhook data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class Webhook:
    """A webhook endpoint.

    Attributes:
        id: Unique identifier for the webhook.
        url: HTTPS URL where webhook events are delivered.
        event_types: List of event types this webhook subscribes to.
        is_active: Whether the webhook is currently enabled.
        is_verified: Whether the webhook URL has been verified.
        consecutive_failures: Number of consecutive delivery failures.
        created_at: When the webhook was created.
        updated_at: When the webhook was last updated.
        description: Optional description of the webhook's purpose.
        disabled_at: When the webhook was automatically disabled due to failures.
        integration_id: ID of the integration this webhook belongs to.
    """

    id: str
    url: str
    event_types: list[str]
    is_active: bool
    is_verified: bool
    consecutive_failures: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    description: str | None = None
    disabled_at: datetime | None = None
    integration_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Webhook:
        return cls(
            id=str(data["id"]),
            url=data["url"],
            event_types=data.get("event_types", []),
            is_active=data["is_active"],
            is_verified=data["is_verified"],
            consecutive_failures=data.get("consecutive_failures", 0),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            description=data.get("description"),
            disabled_at=_parse_datetime(data.get("disabled_at")),
            integration_id=data.get("integration_id"),
        )


@dataclass(frozen=True)
class WebhookCreated:
    """Response after creating a webhook (includes secret shown once).

    Attributes:
        id: Unique identifier for the webhook.
        url: HTTPS URL where webhook events are delivered.
        secret: HMAC signing secret for verifying webhook payloads (shown only once).
        event_types: List of event types this webhook subscribes to.
        is_active: Whether the webhook is currently enabled.
        is_verified: Whether the webhook URL has been verified.
        created_at: When the webhook was created.
        updated_at: When the webhook was last updated.
        description: Optional description of the webhook's purpose.
        integration_id: ID of the integration this webhook belongs to.
    """

    id: str
    url: str
    secret: str
    event_types: list[str]
    is_active: bool
    is_verified: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    description: str | None = None
    integration_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WebhookCreated:
        return cls(
            id=str(data["id"]),
            url=data["url"],
            secret=data["secret"],
            event_types=data.get("event_types", []),
            is_active=data["is_active"],
            is_verified=data["is_verified"],
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            description=data.get("description"),
            integration_id=data.get("integration_id"),
        )


@dataclass(frozen=True)
class WebhookSecret:
    """Response after rotating a webhook secret."""

    secret: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WebhookSecret:
        return cls(secret=data["secret"])
