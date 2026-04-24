"""Inbox thread resource."""

from __future__ import annotations

from typing import Any, cast

from ._base import BaseResource


class Inbox(BaseResource):
    def list_threads(
        self,
        *,
        alias_id: str | None = None,
        domain_id: str | None = None,
        direction: str | None = None,
        include_warmup: bool | None = None,
        q: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "alias_id": alias_id,
            "domain_id": domain_id,
            "direction": direction,
            "include_warmup": include_warmup,
            "q": q,
            "limit": limit,
            "cursor": cursor,
        }
        return cast(dict[str, Any], self._http.request("GET", "/inbox/threads", params=params))

    async def list_threads_async(
        self,
        *,
        alias_id: str | None = None,
        domain_id: str | None = None,
        direction: str | None = None,
        include_warmup: bool | None = None,
        q: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "alias_id": alias_id,
            "domain_id": domain_id,
            "direction": direction,
            "include_warmup": include_warmup,
            "q": q,
            "limit": limit,
            "cursor": cursor,
        }
        return cast(
            dict[str, Any], await self._http.request_async("GET", "/inbox/threads", params=params)
        )

    def get_thread(self, conversation_id: str) -> dict[str, Any]:
        return cast(dict[str, Any], self._http.request("GET", f"/inbox/threads/{conversation_id}"))

    async def get_thread_async(self, conversation_id: str) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            await self._http.request_async("GET", f"/inbox/threads/{conversation_id}"),
        )
