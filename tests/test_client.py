"""Tests for the Bavimail client."""

from __future__ import annotations

import httpx

from bavimail import Bavimail


def test_client_has_all_resources() -> None:
    transport = httpx.MockTransport(lambda r: httpx.Response(200))
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    client = Bavimail(
        api_key="test", base_url="https://test.com", http_client=sync_client
    )
    assert hasattr(client, "domains")
    assert hasattr(client, "aliases")
    assert hasattr(client, "attachments")
    assert hasattr(client, "emails")
    assert hasattr(client, "inbound_emails")
    assert hasattr(client, "conversations")
    assert hasattr(client, "tags")
    assert hasattr(client, "webhooks")
    client.close()


def test_client_context_manager() -> None:
    transport = httpx.MockTransport(lambda r: httpx.Response(200))
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    with Bavimail(
        api_key="test", base_url="https://test.com", http_client=sync_client
    ) as client:
        assert client.domains is not None
