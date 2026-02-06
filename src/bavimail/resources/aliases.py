"""Aliases resource."""

from __future__ import annotations

from typing import Any

from ..models.alias import Alias
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Aliases(BaseResource):
    """Operations on email aliases."""

    def create(self, domain_id: str, alias: str) -> Alias:
        """Create a new alias on a domain."""
        body: dict[str, Any] = {"domain_id": domain_id, "alias": alias}
        data = self._http.request("POST", "/aliases", json=body)
        return Alias.from_dict(data)

    async def create_async(self, domain_id: str, alias: str) -> Alias:
        """Create a new alias on a domain (async)."""
        body: dict[str, Any] = {"domain_id": domain_id, "alias": alias}
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
        data = await self._http.request_async(
            "GET", "/aliases", params=params or None
        )
        return [Alias.from_dict(a) for a in data]

    def get(self, alias_id: str) -> Alias:
        """Get an alias by ID."""
        data = self._http.request("GET", f"/aliases/{alias_id}")
        return Alias.from_dict(data)

    async def get_async(self, alias_id: str) -> Alias:
        """Get an alias by ID (async)."""
        data = await self._http.request_async("GET", f"/aliases/{alias_id}")
        return Alias.from_dict(data)

    def update(self, alias_id: str, alias: str) -> Alias:
        """Rename an alias."""
        data = self._http.request(
            "PUT", f"/aliases/{alias_id}", json={"alias": alias}
        )
        return Alias.from_dict(data)

    async def update_async(self, alias_id: str, alias: str) -> Alias:
        """Rename an alias (async)."""
        data = await self._http.request_async(
            "PUT", f"/aliases/{alias_id}", json={"alias": alias}
        )
        return Alias.from_dict(data)

    def delete(self, alias_id: str) -> None:
        """Delete an alias."""
        self._http.request("DELETE", f"/aliases/{alias_id}")

    async def delete_async(self, alias_id: str) -> None:
        """Delete an alias (async)."""
        await self._http.request_async("DELETE", f"/aliases/{alias_id}")
