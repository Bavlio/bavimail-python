"""Domains resource."""

from __future__ import annotations

from typing import Any

from .._types import UNSET, _UnsetType
from ..models.domain import (
    DNSVerificationResponse,
    Domain,
    DomainSetup,
)
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Domains(BaseResource):
    """Operations on domains."""

    def create(
        self,
        domain: str,
        provider_key: str,
        *,
        provider_config: dict[str, Any] | None = None,
    ) -> Domain:
        """Create a new domain."""
        body: dict[str, Any] = {"domain": domain, "provider_key": provider_key}
        if provider_config is not None:
            body["provider_config"] = provider_config
        data = self._http.request("POST", "/domains", json=body)
        return Domain.from_dict(data)

    async def create_async(
        self,
        domain: str,
        provider_key: str,
        *,
        provider_config: dict[str, Any] | None = None,
    ) -> Domain:
        """Create a new domain (async)."""
        body: dict[str, Any] = {"domain": domain, "provider_key": provider_key}
        if provider_config is not None:
            body["provider_config"] = provider_config
        data = await self._http.request_async("POST", "/domains", json=body)
        return Domain.from_dict(data)

    def list(self) -> _List[Domain]:
        """List all domains."""
        data = self._http.request("GET", "/domains")
        return [Domain.from_dict(d) for d in data]

    async def list_async(self) -> _List[Domain]:
        """List all domains (async)."""
        data = await self._http.request_async("GET", "/domains")
        return [Domain.from_dict(d) for d in data]

    def get(self, domain_id: str) -> Domain:
        """Get a domain by ID."""
        data = self._http.request("GET", f"/domains/{domain_id}")
        return Domain.from_dict(data)

    async def get_async(self, domain_id: str) -> Domain:
        """Get a domain by ID (async)."""
        data = await self._http.request_async("GET", f"/domains/{domain_id}")
        return Domain.from_dict(data)

    def get_setup(self, domain_id: str) -> DomainSetup:
        """Get DNS setup instructions for a domain."""
        data = self._http.request("GET", f"/domains/{domain_id}/setup")
        return DomainSetup.from_dict(data)

    async def get_setup_async(self, domain_id: str) -> DomainSetup:
        """Get DNS setup instructions for a domain (async)."""
        data = await self._http.request_async("GET", f"/domains/{domain_id}/setup")
        return DomainSetup.from_dict(data)

    def get_dns_status(
        self, domain_id: str, *, force_refresh: bool | None = None
    ) -> DNSVerificationResponse:
        """Get live DNS verification status for a domain."""
        params: dict[str, Any] = {}
        if force_refresh is not None:
            params["force_refresh"] = force_refresh
        data = self._http.request("GET", f"/domains/{domain_id}/dns-status", params=params or None)
        return DNSVerificationResponse.from_dict(data)

    async def get_dns_status_async(
        self, domain_id: str, *, force_refresh: bool | None = None
    ) -> DNSVerificationResponse:
        """Get live DNS verification status for a domain (async)."""
        params: dict[str, Any] = {}
        if force_refresh is not None:
            params["force_refresh"] = force_refresh
        data = await self._http.request_async(
            "GET", f"/domains/{domain_id}/dns-status", params=params or None
        )
        return DNSVerificationResponse.from_dict(data)

    def verify(self, domain_id: str, *, force: bool = False) -> Domain:
        """Trigger domain verification."""
        data = self._http.request("POST", f"/domains/{domain_id}/verify", json={"force": force})
        return Domain.from_dict(data)

    async def verify_async(self, domain_id: str, *, force: bool = False) -> Domain:
        """Trigger domain verification (async)."""
        data = await self._http.request_async(
            "POST", f"/domains/{domain_id}/verify", json={"force": force}
        )
        return Domain.from_dict(data)

    def update(
        self,
        domain_id: str,
        *,
        is_active: bool | _UnsetType = UNSET,
        provider_config: dict[str, Any] | _UnsetType = UNSET,
        strip_tracking_on_read: bool | _UnsetType = UNSET,
        extra_retained_headers: _List[str] | _UnsetType = UNSET,
    ) -> Domain:
        """Update a domain."""
        body: dict[str, Any] = {}
        if is_active is not UNSET:
            body["is_active"] = is_active
        if provider_config is not UNSET:
            body["provider_config"] = provider_config
        if strip_tracking_on_read is not UNSET:
            body["strip_tracking_on_read"] = strip_tracking_on_read
        if extra_retained_headers is not UNSET:
            body["extra_retained_headers"] = extra_retained_headers
        data = self._http.request("PUT", f"/domains/{domain_id}", json=body)
        return Domain.from_dict(data)

    async def update_async(
        self,
        domain_id: str,
        *,
        is_active: bool | _UnsetType = UNSET,
        provider_config: dict[str, Any] | _UnsetType = UNSET,
        strip_tracking_on_read: bool | _UnsetType = UNSET,
        extra_retained_headers: _List[str] | _UnsetType = UNSET,
    ) -> Domain:
        """Update a domain (async)."""
        body: dict[str, Any] = {}
        if is_active is not UNSET:
            body["is_active"] = is_active
        if provider_config is not UNSET:
            body["provider_config"] = provider_config
        if strip_tracking_on_read is not UNSET:
            body["strip_tracking_on_read"] = strip_tracking_on_read
        if extra_retained_headers is not UNSET:
            body["extra_retained_headers"] = extra_retained_headers
        data = await self._http.request_async("PUT", f"/domains/{domain_id}", json=body)
        return Domain.from_dict(data)

    def delete(self, domain_id: str) -> None:
        """Delete a domain."""
        self._http.request("DELETE", f"/domains/{domain_id}")

    async def delete_async(self, domain_id: str) -> None:
        """Delete a domain (async)."""
        await self._http.request_async("DELETE", f"/domains/{domain_id}")
