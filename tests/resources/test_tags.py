"""Tests for the Tags resource."""

from __future__ import annotations

import httpx

from tests.conftest import (
    SAMPLE_TAG,
    json_response,
    make_client,
    no_content_response,
)


def test_create_tag() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        body = request.content.decode()
        assert "important" in body
        return json_response(SAMPLE_TAG, status_code=200)

    client = make_client("https://test.com", "key", handler)
    tag = client.tags.create("important")
    assert tag.name == "important"
    client.close()


def test_create_tag_with_options() -> None:
    custom_tag = {**SAMPLE_TAG, "color": "#ff0000", "is_pinned": True}

    def handler(request: httpx.Request) -> httpx.Response:
        body = request.content.decode()
        assert "#ff0000" in body
        return json_response(custom_tag)

    client = make_client("https://test.com", "key", handler)
    tag = client.tags.create("important", color="#ff0000", is_pinned=True)
    assert tag.color == "#ff0000"
    client.close()


def test_list_tags() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response([SAMPLE_TAG])

    client = make_client("https://test.com", "key", handler)
    tags = client.tags.list()
    assert len(tags) == 1
    client.close()


def test_get_tag() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(SAMPLE_TAG)

    client = make_client("https://test.com", "key", handler)
    tag = client.tags.get(SAMPLE_TAG["id"])
    assert tag.id == SAMPLE_TAG["id"]
    client.close()


def test_update_tag() -> None:
    updated = {**SAMPLE_TAG, "name": "critical"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        body = request.content.decode()
        assert "critical" in body
        return json_response(updated)

    client = make_client("https://test.com", "key", handler)
    tag = client.tags.update(SAMPLE_TAG["id"], name="critical")
    assert tag.name == "critical"
    client.close()


def test_delete_tag() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.tags.delete(SAMPLE_TAG["id"])
    client.close()
