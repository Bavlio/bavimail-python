"""Integration data models for B2B service-level operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class IntegrationInfo:
    """Information about an available integration.

    Attributes:
        id: Unique identifier for the integration.
        display_name: Human-readable name of the integration.
        auth_mode: Authentication mode used by the integration (e.g., 'hmac').
    """

    id: str
    display_name: str
    auth_mode: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntegrationInfo:
        return cls(
            id=str(data["id"]),
            display_name=data["display_name"],
            auth_mode=data["auth_mode"],
        )


@dataclass(frozen=True)
class BootstrapApiKeyResponse:
    """Response from bootstrapping an API key for a user.

    Attributes:
        api_key: The generated or existing API key.
        created: Whether a new API key was created (False if existing key returned).
        expires_at: When the API key expires, if applicable.
    """

    api_key: str
    created: bool
    expires_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BootstrapApiKeyResponse:
        return cls(
            api_key=data["api_key"],
            created=data["created"],
            expires_at=_parse_datetime(data.get("expires_at")),
        )


@dataclass(frozen=True)
class RevokeApiKeyResponse:
    """Response from revoking an API key.

    Attributes:
        revoked: Whether the API key was successfully revoked.
    """

    revoked: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RevokeApiKeyResponse:
        return cls(revoked=data["revoked"])
