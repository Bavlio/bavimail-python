"""Inbound emails resource."""

from __future__ import annotations

from typing import Any

from ..models.inbound_email import InboundEmailDetail, InboundEmailSummary
from ..models.tag import EmailTag
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class InboundEmails(BaseResource):
    """Operations on inbound (received) emails."""

    def list(
        self,
        *,
        alias_id: str | None = None,
        tag_ids: _List[str] | None = None,
        tag_match: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[InboundEmailSummary]:
        """List inbound emails."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if tag_ids is not None:
            params["tag_ids"] = ",".join(tag_ids)
        if tag_match is not None:
            params["tag_match"] = tag_match
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.request("GET", "/inbound-emails", params=params or None)
        return [InboundEmailSummary.from_dict(e) for e in data]

    async def list_async(
        self,
        *,
        alias_id: str | None = None,
        tag_ids: _List[str] | None = None,
        tag_match: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[InboundEmailSummary]:
        """List inbound emails (async)."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if tag_ids is not None:
            params["tag_ids"] = ",".join(tag_ids)
        if tag_match is not None:
            params["tag_match"] = tag_match
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = await self._http.request_async(
            "GET", "/inbound-emails", params=params or None
        )
        return [InboundEmailSummary.from_dict(e) for e in data]

    def get(self, email_id: str) -> InboundEmailDetail:
        """Get full detail of an inbound email."""
        data = self._http.request("GET", f"/inbound-emails/{email_id}")
        return InboundEmailDetail.from_dict(data)

    async def get_async(self, email_id: str) -> InboundEmailDetail:
        """Get full detail of an inbound email (async)."""
        data = await self._http.request_async("GET", f"/inbound-emails/{email_id}")
        return InboundEmailDetail.from_dict(data)

    def download_raw(self, email_id: str) -> bytes:
        """Download raw RFC822 email bytes."""
        return self._http.request_bytes("GET", f"/inbound-emails/{email_id}/raw")

    async def download_raw_async(self, email_id: str) -> bytes:
        """Download raw RFC822 email bytes (async)."""
        return await self._http.request_bytes_async(
            "GET", f"/inbound-emails/{email_id}/raw"
        )

    def download_attachment(self, email_id: str, index: int) -> bytes:
        """Download an attachment by index."""
        return self._http.request_bytes(
            "GET", f"/inbound-emails/{email_id}/attachments/{index}"
        )

    async def download_attachment_async(self, email_id: str, index: int) -> bytes:
        """Download an attachment by index (async)."""
        return await self._http.request_bytes_async(
            "GET", f"/inbound-emails/{email_id}/attachments/{index}"
        )

    def delete(self, email_id: str) -> None:
        """Delete an inbound email."""
        self._http.request("DELETE", f"/inbound-emails/{email_id}")

    async def delete_async(self, email_id: str) -> None:
        """Delete an inbound email (async)."""
        await self._http.request_async("DELETE", f"/inbound-emails/{email_id}")

    def add_tags(
        self,
        email_id: str,
        tag_ids: _List[str],
        *,
        note: str | None = None,
    ) -> _List[EmailTag]:
        """Add tags to an inbound email."""
        body: dict[str, Any] = {"tag_ids": tag_ids}
        if note is not None:
            body["note"] = note
        data = self._http.request(
            "POST", f"/inbound-emails/{email_id}/tags", json=body
        )
        return [EmailTag.from_dict(t) for t in data]

    async def add_tags_async(
        self,
        email_id: str,
        tag_ids: _List[str],
        *,
        note: str | None = None,
    ) -> _List[EmailTag]:
        """Add tags to an inbound email (async)."""
        body: dict[str, Any] = {"tag_ids": tag_ids}
        if note is not None:
            body["note"] = note
        data = await self._http.request_async(
            "POST", f"/inbound-emails/{email_id}/tags", json=body
        )
        return [EmailTag.from_dict(t) for t in data]

    def get_tags(self, email_id: str) -> _List[EmailTag]:
        """Get tags applied to an inbound email."""
        data = self._http.request("GET", f"/inbound-emails/{email_id}/tags")
        return [EmailTag.from_dict(t) for t in data]

    async def get_tags_async(self, email_id: str) -> _List[EmailTag]:
        """Get tags applied to an inbound email (async)."""
        data = await self._http.request_async(
            "GET", f"/inbound-emails/{email_id}/tags"
        )
        return [EmailTag.from_dict(t) for t in data]

    def replace_tags(
        self,
        email_id: str,
        tag_ids: _List[str],
        *,
        note: str | None = None,
    ) -> _List[EmailTag]:
        """Replace all tags on an inbound email."""
        body: dict[str, Any] = {"tag_ids": tag_ids}
        if note is not None:
            body["note"] = note
        data = self._http.request(
            "PUT", f"/inbound-emails/{email_id}/tags", json=body
        )
        return [EmailTag.from_dict(t) for t in data]

    async def replace_tags_async(
        self,
        email_id: str,
        tag_ids: _List[str],
        *,
        note: str | None = None,
    ) -> _List[EmailTag]:
        """Replace all tags on an inbound email (async)."""
        body: dict[str, Any] = {"tag_ids": tag_ids}
        if note is not None:
            body["note"] = note
        data = await self._http.request_async(
            "PUT", f"/inbound-emails/{email_id}/tags", json=body
        )
        return [EmailTag.from_dict(t) for t in data]

    def remove_tag(self, email_id: str, tag_id: str) -> None:
        """Remove a tag from an inbound email."""
        self._http.request(
            "DELETE", f"/inbound-emails/{email_id}/tags/{tag_id}"
        )

    async def remove_tag_async(self, email_id: str, tag_id: str) -> None:
        """Remove a tag from an inbound email (async)."""
        await self._http.request_async(
            "DELETE", f"/inbound-emails/{email_id}/tags/{tag_id}"
        )
