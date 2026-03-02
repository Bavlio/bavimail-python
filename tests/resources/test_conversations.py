"""Tests for the Conversations resource."""

from __future__ import annotations

import httpx

from tests.conftest import SAMPLE_CONVERSATION, json_response, make_client


def test_list_conversations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return json_response([SAMPLE_CONVERSATION])

    client = make_client("https://test.com", "key", handler)
    conversations = client.conversations.list()
    assert len(conversations) == 1
    assert conversations[0].subject == "Test conversation"
    client.close()


def test_list_conversations_with_filters() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        assert "alias_id" in url_str
        return json_response([SAMPLE_CONVERSATION])

    client = make_client("https://test.com", "key", handler)
    conversations = client.conversations.list(alias_id="a1")
    assert len(conversations) == 1
    client.close()


def test_list_conversations_with_include_warmup() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.params["include_warmup"] == "true"
        return json_response([SAMPLE_CONVERSATION])

    client = make_client("https://test.com", "key", handler)
    conversations = client.conversations.list(include_warmup=True)
    assert len(conversations) == 1
    client.close()


def test_get_conversation() -> None:
    detail = {
        **SAMPLE_CONVERSATION,
        "messages": [
            {
                "id": "m1",
                "direction": "inbound",
                "from_email": "sender@test.com",
                "to_email": "support@example.com",
                "subject": "Hi",
                "attachment_count": 0,
                "timestamp": "2025-01-01T00:00:00Z",
            }
        ],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(detail)

    client = make_client("https://test.com", "key", handler)
    conv = client.conversations.get(SAMPLE_CONVERSATION["id"])
    assert conv.message_count == 2
    assert len(conv.messages) == 1
    client.close()
