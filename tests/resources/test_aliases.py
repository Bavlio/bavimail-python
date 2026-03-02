"""Tests for the Aliases resource."""

from __future__ import annotations

import json

import httpx

from tests.conftest import (
    SAMPLE_ALIAS,
    json_response,
    make_client,
    no_content_response,
)


def test_create_alias() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/aliases" in str(request.url)
        return json_response(SAMPLE_ALIAS, status_code=200)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.create(SAMPLE_ALIAS["domain_id"], "support")
    assert alias.alias == "support"
    assert alias.full_email == "support@example.com"
    client.close()


def test_list_aliases() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response([SAMPLE_ALIAS])

    client = make_client("https://test.com", "key", handler)
    aliases = client.aliases.list()
    assert len(aliases) == 1
    client.close()


def test_list_aliases_with_domain_filter() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "domain_id" in str(request.url)
        return json_response([SAMPLE_ALIAS])

    client = make_client("https://test.com", "key", handler)
    aliases = client.aliases.list(domain_id=SAMPLE_ALIAS["domain_id"])
    assert len(aliases) == 1
    client.close()


def test_get_alias() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(SAMPLE_ALIAS)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.get(SAMPLE_ALIAS["id"])
    assert alias.id == SAMPLE_ALIAS["id"]
    client.close()


def test_update_alias() -> None:
    updated = {**SAMPLE_ALIAS, "alias": "info", "full_email": "info@example.com"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        return json_response(updated)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.update(SAMPLE_ALIAS["id"], alias="info")
    assert alias.alias == "info"
    client.close()


def test_create_alias_with_signature() -> None:
    alias_with_sig = {
        **SAMPLE_ALIAS,
        "signature_html": "<p>Best regards</p>",
        "signature_text": "Best regards",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        body = json.loads(request.content)
        assert body["signature_html"] == "<p>Best regards</p>"
        return json_response(alias_with_sig)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.create(
        SAMPLE_ALIAS["domain_id"],
        "support",
        signature_html="<p>Best regards</p>",
    )
    assert alias.signature_html == "<p>Best regards</p>"
    client.close()


def test_update_alias_with_signature() -> None:
    updated = {
        **SAMPLE_ALIAS,
        "signature_html": "<p>Cheers</p>",
        "signature_text": "Cheers",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        body = json.loads(request.content)
        assert body["signature_html"] == "<p>Cheers</p>"
        return json_response(updated)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.update(
        SAMPLE_ALIAS["id"],
        signature_html="<p>Cheers</p>",
    )
    assert alias.signature_html == "<p>Cheers</p>"
    client.close()


def test_delete_alias() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.aliases.delete(SAMPLE_ALIAS["id"])
    client.close()


def test_set_warmup_token() -> None:
    alias_response = {**SAMPLE_ALIAS, "warmup_token": "motor-graph"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        assert str(request.url).endswith(f"/aliases/{SAMPLE_ALIAS['id']}/warmup-token")
        body = json.loads(request.content)
        assert body["token"] == "motor-graph"
        return json_response(alias_response)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.set_warmup_token(SAMPLE_ALIAS["id"], "motor-graph")
    assert alias.warmup_token == "motor-graph"
    client.close()


def test_clear_warmup_token() -> None:
    alias_response = {**SAMPLE_ALIAS, "warmup_token": None}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        assert str(request.url).endswith(f"/aliases/{SAMPLE_ALIAS['id']}/warmup-token")
        return json_response(alias_response)

    client = make_client("https://test.com", "key", handler)
    alias = client.aliases.clear_warmup_token(SAMPLE_ALIAS["id"])
    assert alias.warmup_token is None
    client.close()
