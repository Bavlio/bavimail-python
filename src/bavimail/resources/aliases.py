"""Aliases resource."""

from __future__ import annotations

from typing import Any

from .._types import UNSET, _UnsetType
from ..models.alias import Alias
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Aliases(BaseResource):
    """Operations on email aliases."""

    def create(
        self,
        domain_id: str,
        alias: str,
        *,
        signature_html: str | None = None,
    ) -> Alias:
        """Create a new alias on a domain."""
        body: dict[str, Any] = {"domain_id": domain_id, "alias": alias}
        if signature_html is not None:
            body["signature_html"] = signature_html
        data = self._http.request("POST", "/aliases", json=body)
        return Alias.from_dict(data)

    async def create_async(
        self,
        domain_id: str,
        alias: str,
        *,
        signature_html: str | None = None,
    ) -> Alias:
        """Create a new alias on a domain (async)."""
        body: dict[str, Any] = {"domain_id": domain_id, "alias": alias}
        if signature_html is not None:
            body["signature_html"] = signature_html
        data = await self._http.request_async("POST", "/aliases", json=body)
        return Alias.from_dict(data)

    def list(self, *, domain_id: str | None = None) -> _List[Alias]:
        """List aliases, optionally filtered by domain."""
        params: dict[str, Any] = {}
        if domain_id is not None:
            params["domain_id"] = domain_id
        data = self._http.request("GET", "/aliases", params=params or None)
        return [Alias.from_dict(a) for a in data]

    async def list_async(self, *, domain_id: str | None = None) -> _List[Alias]:
        """List aliases, optionally filtered by domain (async)."""
        params: dict[str, Any] = {}
        if domain_id is not None:
            params["domain_id"] = domain_id
        data = await self._http.request_async("GET", "/aliases", params=params or None)
        return [Alias.from_dict(a) for a in data]

    def get(self, alias_id: str) -> Alias:
        """Get an alias by ID."""
        data = self._http.request("GET", f"/aliases/{alias_id}")
        return Alias.from_dict(data)

    async def get_async(self, alias_id: str) -> Alias:
        """Get an alias by ID (async)."""
        data = await self._http.request_async("GET", f"/aliases/{alias_id}")
        return Alias.from_dict(data)

    def update(
        self,
        alias_id: str,
        *,
        alias: str | _UnsetType = UNSET,
        signature_html: str | None | _UnsetType = UNSET,
    ) -> Alias:
        """Update an alias."""
        body: dict[str, Any] = {}
        if alias is not UNSET:
            body["alias"] = alias
        if signature_html is not UNSET:
            body["signature_html"] = signature_html
        data = self._http.request("PUT", f"/aliases/{alias_id}", json=body)
        return Alias.from_dict(data)

    async def update_async(
        self,
        alias_id: str,
        *,
        alias: str | _UnsetType = UNSET,
        signature_html: str | None | _UnsetType = UNSET,
    ) -> Alias:
        """Update an alias (async)."""
        body: dict[str, Any] = {}
        if alias is not UNSET:
            body["alias"] = alias
        if signature_html is not UNSET:
            body["signature_html"] = signature_html
        data = await self._http.request_async("PUT", f"/aliases/{alias_id}", json=body)
        return Alias.from_dict(data)

    def delete(self, alias_id: str) -> None:
        """Delete an alias."""
        self._http.request("DELETE", f"/aliases/{alias_id}")

    async def delete_async(self, alias_id: str) -> None:
        """Delete an alias (async)."""
        await self._http.request_async("DELETE", f"/aliases/{alias_id}")

    def set_warmup_token(self, alias_id: str, token: str) -> Alias:
        """Set warmup token for an alias."""
        data = self._http.request(
            "PUT",
            f"/aliases/{alias_id}/warmup-token",
            json={"token": token},
        )
        return Alias.from_dict(data)

    async def set_warmup_token_async(self, alias_id: str, token: str) -> Alias:
        """Set warmup token for an alias (async)."""
        data = await self._http.request_async(
            "PUT",
            f"/aliases/{alias_id}/warmup-token",
            json={"token": token},
        )
        return Alias.from_dict(data)

    def clear_warmup_token(self, alias_id: str) -> Alias:
        """Clear warmup token for an alias."""
        data = self._http.request(
            "DELETE",
            f"/aliases/{alias_id}/warmup-token",
        )
        return Alias.from_dict(data)

    async def clear_warmup_token_async(self, alias_id: str) -> Alias:
        """Clear warmup token for an alias (async)."""
        data = await self._http.request_async(
            "DELETE",
            f"/aliases/{alias_id}/warmup-token",
        )
        return Alias.from_dict(data)
