"""Attachment storage resource."""

from __future__ import annotations

from typing import Any

from ..models.attachment import AttachmentFile, AttachmentUploadFile, AttachmentUploadResponse
from ._base import BaseResource


class Attachments(BaseResource):
    """Operations on stored attachments."""

    def upload(self, files: list[AttachmentUploadFile]) -> AttachmentUploadResponse:
        """Upload one or more files into attachment storage."""
        payload = [
            (
                "files",
                (
                    item.filename,
                    item.content,
                    item.mime_type or "application/octet-stream",
                ),
            )
            for item in files
        ]
        data = self._http.request("POST", "/attachments", files=payload)
        return AttachmentUploadResponse.from_dict(data)

    async def upload_async(self, files: list[AttachmentUploadFile]) -> AttachmentUploadResponse:
        """Upload one or more files into attachment storage (async)."""
        payload = [
            (
                "files",
                (
                    item.filename,
                    item.content,
                    item.mime_type or "application/octet-stream",
                ),
            )
            for item in files
        ]
        data = await self._http.request_async("POST", "/attachments", files=payload)
        return AttachmentUploadResponse.from_dict(data)

    def get(self, attachment_id: str) -> AttachmentFile:
        """Get stored attachment metadata."""
        data = self._http.request("GET", f"/attachments/{attachment_id}")
        return AttachmentFile.from_dict(data)

    async def get_async(self, attachment_id: str) -> AttachmentFile:
        """Get stored attachment metadata (async)."""
        data = await self._http.request_async("GET", f"/attachments/{attachment_id}")
        return AttachmentFile.from_dict(data)

    def download(self, attachment_id: str, *, inline: bool = False) -> bytes:
        """Download attachment bytes."""
        return self._http.request_bytes(
            "GET",
            f"/attachments/{attachment_id}/download",
            params={"inline": inline},
        )

    async def download_async(self, attachment_id: str, *, inline: bool = False) -> bytes:
        """Download attachment bytes (async)."""
        return await self._http.request_bytes_async(
            "GET",
            f"/attachments/{attachment_id}/download",
            params={"inline": inline},
        )
