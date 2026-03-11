"""Tests for the Attachments resource."""

from __future__ import annotations

import httpx

from bavimail import AttachmentUploadFile
from tests.conftest import json_response, make_client


SAMPLE_ATTACHMENT = {
    "id": "att-0000-0000-0000-000000000001",
    "user_id": "u1000000-0000-0000-0000-000000000001",
    "filename": "invoice.pdf",
    "size_bytes": 1234,
    "mime_type": "application/pdf",
    "sha256": "abc123",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}


def test_upload_attachments() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/attachments" in str(request.url)
        assert b"invoice.pdf" in request.content
        return json_response({
            "attachments": [SAMPLE_ATTACHMENT],
            "uploaded_at": "2025-01-01T00:00:00Z",
        })

    client = make_client("https://test.com", "key", handler)
    response = client.attachments.upload([
        AttachmentUploadFile(
            filename="invoice.pdf",
            content=b"pdf-bytes",
            mime_type="application/pdf",
        )
    ])
    assert len(response.attachments) == 1
    assert response.attachments[0].filename == "invoice.pdf"
    client.close()


def test_get_attachment() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return json_response(SAMPLE_ATTACHMENT)

    client = make_client("https://test.com", "key", handler)
    attachment = client.attachments.get(SAMPLE_ATTACHMENT["id"])
    assert attachment.id == SAMPLE_ATTACHMENT["id"]
    client.close()


def test_download_attachment() -> None:
    attachment_bytes = b"PDF content here"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert SAMPLE_ATTACHMENT["id"] in str(request.url)
        return httpx.Response(200, content=attachment_bytes)

    client = make_client("https://test.com", "key", handler)
    data = client.attachments.download(SAMPLE_ATTACHMENT["id"])
    assert data == attachment_bytes
    client.close()
