"""Emails (outbound) resource."""

from __future__ import annotations

from typing import Any

from ..models.email import BatchEmailResponse, Email, EmailClick, TrackedLink
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
        track_clicks: bool = False,
        click_tracking_patterns: _List[str] | None = None,
        send_at: str | None = None,
        send_at_timezone: str | None = None,
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
        if track_clicks:
            payload["track_clicks"] = track_clicks
        if click_tracking_patterns is not None:
            payload["click_tracking_patterns"] = click_tracking_patterns
        if send_at is not None:
            payload["send_at"] = send_at
        if send_at_timezone is not None:
            payload["send_at_timezone"] = send_at_timezone
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
        track_clicks: bool = False,
        click_tracking_patterns: _List[str] | None = None,
        send_at: str | None = None,
        send_at_timezone: str | None = None,
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
        if track_clicks:
            payload["track_clicks"] = track_clicks
        if click_tracking_patterns is not None:
            payload["click_tracking_patterns"] = click_tracking_patterns
        if send_at is not None:
            payload["send_at"] = send_at
        if send_at_timezone is not None:
            payload["send_at_timezone"] = send_at_timezone
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

    def batch_send(self, emails: _List[dict[str, Any]]) -> BatchEmailResponse:
        """Send a batch of emails."""
        data = self._http.request("POST", "/emails/batch", json=emails)
        return BatchEmailResponse.from_dict(data)

    async def batch_send_async(
        self, emails: _List[dict[str, Any]]
    ) -> BatchEmailResponse:
        """Send a batch of emails (async)."""
        data = await self._http.request_async(
            "POST", "/emails/batch", json=emails
        )
        return BatchEmailResponse.from_dict(data)

    def cancel(self, email_id: str) -> Email:
        """Cancel a scheduled email."""
        data = self._http.request("POST", f"/emails/{email_id}/cancel")
        return Email.from_dict(data)

    async def cancel_async(self, email_id: str) -> Email:
        """Cancel a scheduled email (async)."""
        data = await self._http.request_async(
            "POST", f"/emails/{email_id}/cancel"
        )
        return Email.from_dict(data)

    def list_clicks(
        self,
        email_id: str,
        *,
        link_id: str | None = None,
        include_bots: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[EmailClick]:
        """List click events for an email."""
        params: dict[str, Any] = {}
        if link_id is not None:
            params["link_id"] = link_id
        if include_bots is not None:
            params["include_bots"] = include_bots
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = self._http.request(
            "GET", f"/emails/{email_id}/clicks", params=params or None
        )
        return [EmailClick.from_dict(c) for c in data["clicks"]]

    async def list_clicks_async(
        self,
        email_id: str,
        *,
        link_id: str | None = None,
        include_bots: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> _List[EmailClick]:
        """List click events for an email (async)."""
        params: dict[str, Any] = {}
        if link_id is not None:
            params["link_id"] = link_id
        if include_bots is not None:
            params["include_bots"] = include_bots
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data = await self._http.request_async(
            "GET", f"/emails/{email_id}/clicks", params=params or None
        )
        return [EmailClick.from_dict(c) for c in data["clicks"]]

    def list_links(self, email_id: str) -> _List[TrackedLink]:
        """List tracked links for an email."""
        data = self._http.request("GET", f"/emails/{email_id}/links")
        return [TrackedLink.from_dict(l) for l in data]

    async def list_links_async(self, email_id: str) -> _List[TrackedLink]:
        """List tracked links for an email (async)."""
        data = await self._http.request_async(
            "GET", f"/emails/{email_id}/links"
        )
        return [TrackedLink.from_dict(l) for l in data]
