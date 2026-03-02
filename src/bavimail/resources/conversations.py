"""Conversations resource."""

from __future__ import annotations

from typing import Any

from ..models.conversation import ConversationDetail, ConversationSummary
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Conversations(BaseResource):
    """Operations on conversation threads."""

    def list(
        self,
        *,
        alias_id: str | None = None,
        domain_id: str | None = None,
        include_warmup: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[ConversationSummary]:
        """List conversations ordered by most recent activity."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if domain_id is not None:
            params["domain_id"] = domain_id
        if include_warmup is not None:
            params["include_warmup"] = include_warmup
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.request(
            "GET", "/conversations", params=params or None
        )
        return [ConversationSummary.from_dict(c) for c in data]

    async def list_async(
        self,
        *,
        alias_id: str | None = None,
        domain_id: str | None = None,
        include_warmup: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[ConversationSummary]:
        """List conversations ordered by most recent activity (async)."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if domain_id is not None:
            params["domain_id"] = domain_id
        if include_warmup is not None:
            params["include_warmup"] = include_warmup
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = await self._http.request_async(
            "GET", "/conversations", params=params or None
        )
        return [ConversationSummary.from_dict(c) for c in data]

    def get(self, conversation_id: str) -> ConversationDetail:
        """Get full conversation detail with all messages."""
        data = self._http.request("GET", f"/conversations/{conversation_id}")
        return ConversationDetail.from_dict(data)

    async def get_async(self, conversation_id: str) -> ConversationDetail:
        """Get full conversation detail with all messages (async)."""
        data = await self._http.request_async(
            "GET", f"/conversations/{conversation_id}"
        )
        return ConversationDetail.from_dict(data)
