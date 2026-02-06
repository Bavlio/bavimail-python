"""Emails (outbound) resource."""

from __future__ import annotations

from typing import Any

from ..models.email import Email
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Emails(BaseResource):
    """Operations on outbound emails."""

    def send(
        self,
        alias_id: str,
        to_email: str,
        subject: str,
        body: str,
        *,
        track_opens: bool = True,
        conversation_id: str | None = None,
        in_reply_to: str | None = None,
        attachments: _List[dict[str, Any]] | None = None,
    ) -> Email:
        """Send an email from a verified alias."""
        payload: dict[str, Any] = {
            "alias_id": alias_id,
            "to_email": to_email,
            "subject": subject,
            "body": body,
            "track_opens": track_opens,
        }
        if conversation_id is not None:
            payload["conversation_id"] = conversation_id
        if in_reply_to is not None:
            payload["in_reply_to"] = in_reply_to
        if attachments is not None:
            payload["attachments"] = attachments
        data = self._http.request("POST", "/emails", json=payload)
        return Email.from_dict(data)

    async def send_async(
        self,
        alias_id: str,
        to_email: str,
        subject: str,
        body: str,
        *,
        track_opens: bool = True,
        conversation_id: str | None = None,
        in_reply_to: str | None = None,
        attachments: _List[dict[str, Any]] | None = None,
    ) -> Email:
        """Send an email from a verified alias (async)."""
        payload: dict[str, Any] = {
            "alias_id": alias_id,
            "to_email": to_email,
            "subject": subject,
            "body": body,
            "track_opens": track_opens,
        }
        if conversation_id is not None:
            payload["conversation_id"] = conversation_id
        if in_reply_to is not None:
            payload["in_reply_to"] = in_reply_to
        if attachments is not None:
            payload["attachments"] = attachments
        data = await self._http.request_async("POST", "/emails", json=payload)
        return Email.from_dict(data)

    def list(
        self,
        *,
        alias_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[Email]:
        """List sent emails."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.request("GET", "/emails", params=params or None)
        return [Email.from_dict(e) for e in data]

    async def list_async(
        self,
        *,
        alias_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[Email]:
        """List sent emails (async)."""
        params: dict[str, Any] = {}
        if alias_id is not None:
            params["alias_id"] = alias_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = await self._http.request_async(
            "GET", "/emails", params=params or None
        )
        return [Email.from_dict(e) for e in data]

    def get(self, email_id: str) -> Email:
        """Get an email by ID."""
        data = self._http.request("GET", f"/emails/{email_id}")
        return Email.from_dict(data)

    async def get_async(self, email_id: str) -> Email:
        """Get an email by ID (async)."""
        data = await self._http.request_async("GET", f"/emails/{email_id}")
        return Email.from_dict(data)
