"""Suppressions resource."""

from __future__ import annotations

from typing import Any

from ..models.suppression import Suppression
from ._base import BaseResource

_List = list


class Suppressions(BaseResource):
    def list(
        self,
        *,
        status: str | None = None,
        reason: str | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[Suppression]:
        params = {
            "status": status,
            "reason": reason,
            "search": search,
            "limit": limit,
            "offset": offset,
        }
        data = self._http.request("GET", "/suppressions", params=params)
        return [Suppression.from_dict(s) for s in data]

    async def list_async(
        self,
        *,
        status: str | None = None,
        reason: str | None = None,
        search: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[Suppression]:
        params = {
            "status": status,
            "reason": reason,
            "search": search,
            "limit": limit,
            "offset": offset,
        }
        data = await self._http.request_async("GET", "/suppressions", params=params)
        return [Suppression.from_dict(s) for s in data]

    def create(
        self,
        email: str,
        reason: str,
        *,
        source: str | None = None,
        note: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Suppression:
        body = {
            "email": email,
            "reason": reason,
            "source": source,
            "note": note,
            "metadata": metadata,
        }
        data = self._http.request("POST", "/suppressions", json=body)
        return Suppression.from_dict(data)

    async def create_async(
        self,
        email: str,
        reason: str,
        *,
        source: str | None = None,
        note: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Suppression:
        body = {
            "email": email,
            "reason": reason,
            "source": source,
            "note": note,
            "metadata": metadata,
        }
        data = await self._http.request_async("POST", "/suppressions", json=body)
        return Suppression.from_dict(data)

    def release(self, suppression_id: str) -> Suppression:
        data = self._http.request("POST", f"/suppressions/{suppression_id}/release")
        return Suppression.from_dict(data)

    async def release_async(self, suppression_id: str) -> Suppression:
        data = await self._http.request_async("POST", f"/suppressions/{suppression_id}/release")
        return Suppression.from_dict(data)
