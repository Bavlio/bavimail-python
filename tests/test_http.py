"""Tests for the HTTP client layer."""

from __future__ import annotations

import httpx
import pytest

from bavimail._http import HttpClient
from bavimail.exceptions import NotFoundError


def test_request_uses_path_directly() -> None:
    """Verify that paths are used as-is (no prefix added)."""
    captured_url = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_url
        captured_url = str(request.url)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    http = HttpClient(
        base_url="https://test.com",
        api_key="key",
        http_client=sync_client,
    )
    http.request("GET", "/domains")
    assert captured_url is not None
    assert captured_url == "https://test.com/domains"


def test_request_sends_api_key_header() -> None:
    captured_headers: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_headers.update(dict(request.headers))
        return httpx.Response(200, json={})

    transport = httpx.MockTransport(handler)
    sync_client = httpx.Client(
        transport=transport,
        base_url="https://test.com",
        headers={"x-api-key": "my-key", "User-Agent": "test"},
    )
    http = HttpClient(
        base_url="https://test.com",
        api_key="my-key",
        http_client=sync_client,
    )
    http.request("GET", "/test")
    assert captured_headers.get("x-api-key") == "my-key"


def test_request_raises_on_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"detail": {"message": "Not found", "code": "DOMAIN_NOT_FOUND"}},
            headers={"x-request-id": "req-1"},
        )

    transport = httpx.MockTransport(handler)
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    http = HttpClient(
        base_url="https://test.com",
        api_key="key",
        http_client=sync_client,
    )
    with pytest.raises(NotFoundError) as exc_info:
        http.request("GET", "/domains/123")
    assert exc_info.value.request_id == "req-1"


def test_request_204_returns_none() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    http = HttpClient(
        base_url="https://test.com",
        api_key="key",
        http_client=sync_client,
    )
    result = http.request("DELETE", "/domains/123")
    assert result is None


def test_clean_params_removes_none() -> None:
    result = HttpClient._clean_params({"a": 1, "b": None, "c": "x"})
    assert result == {"a": 1, "c": "x"}


def test_clean_params_none_input() -> None:
    assert HttpClient._clean_params(None) is None


def test_request_bytes_returns_content() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"raw email content")

    transport = httpx.MockTransport(handler)
    sync_client = httpx.Client(transport=transport, base_url="https://test.com")
    http = HttpClient(
        base_url="https://test.com",
        api_key="key",
        http_client=sync_client,
    )
    data = http.request_bytes("GET", "/inbound-emails/123/raw")
    assert data == b"raw email content"


def test_base_url_trailing_slash_stripped() -> None:
    http = HttpClient(base_url="https://test.com/", api_key="key")
    assert http._base_url == "https://test.com"
