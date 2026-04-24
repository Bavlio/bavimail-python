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
        direction: str | None = None,
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
        if direction is not None:
            params["direction"] = direction
        if include_warmup is not None:
            params["include_warmup"] = include_warmup
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.request("GET", "/conversations", params=params or None)
        return [ConversationSummary.from_dict(c) for c in data]

    async def list_async(
        self,
        *,
        alias_id: str | None = None,
        domain_id: str | None = None,
        direction: str | None = None,
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
        if direction is not None:
            params["direction"] = direction
        if include_warmup is not None:
            params["include_warmup"] = include_warmup
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = await self._http.request_async("GET", "/conversations", params=params or None)
        return [ConversationSummary.from_dict(c) for c in data]

    def get(self, conversation_id: str) -> ConversationDetail:
        """Get full conversation detail with all messages."""
        data = self._http.request("GET", f"/conversations/{conversation_id}")
        return ConversationDetail.from_dict(data)

    async def get_async(self, conversation_id: str) -> ConversationDetail:
        """Get full conversation detail with all messages (async)."""
        data = await self._http.request_async("GET", f"/conversations/{conversation_id}")
        return ConversationDetail.from_dict(data)

    def mark_read(self, conversation_id: str) -> None:
        """Mark a conversation's inbound messages as read."""
        self._http.request("POST", f"/conversations/{conversation_id}/mark-read")

    async def mark_read_async(self, conversation_id: str) -> None:
        """Mark a conversation's inbound messages as read (async)."""
        await self._http.request_async("POST", f"/conversations/{conversation_id}/mark-read")

    def mark_unread(self, conversation_id: str) -> None:
        """Mark a conversation's inbound messages as unread."""
        self._http.request("POST", f"/conversations/{conversation_id}/mark-unread")

    async def mark_unread_async(self, conversation_id: str) -> None:
        """Mark a conversation's inbound messages as unread (async)."""
        await self._http.request_async("POST", f"/conversations/{conversation_id}/mark-unread")

    def delete(self, conversation_id: str) -> None:
        """Delete a conversation and its messages."""
        self._http.request("DELETE", f"/conversations/{conversation_id}")

    async def delete_async(self, conversation_id: str) -> None:
        """Delete a conversation and its messages (async)."""
        await self._http.request_async("DELETE", f"/conversations/{conversation_id}")
