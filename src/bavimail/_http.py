"""HTTP transport layer wrapping httpx for sync and async requests."""

from __future__ import annotations

from typing import Any

import httpx

from ._version import __version__
from .exceptions import _raise_for_status


class HttpClient:
    """Low-level HTTP client that wraps httpx for both sync and async usage.

    Lazily creates clients so sync-only users never instantiate an async client.
    """

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
        async_http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self._base_url = base_url
        self._api_key = api_key
        self._timeout = timeout
        self._custom_client = http_client
        self._custom_async_client = async_http_client
        self._client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    @property
    def _default_headers(self) -> dict[str, str]:
        return {
            "x-api-key": self._api_key,
            "User-Agent": f"bavimail-python/{__version__}",
            "Accept": "application/json",
        }

    def _get_client(self) -> httpx.Client:
        if self._custom_client is not None:
            return self._custom_client
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                headers=self._default_headers,
                timeout=self._timeout,
            )
        return self._client

    def _get_async_client(self) -> httpx.AsyncClient:
        if self._custom_async_client is not None:
            return self._custom_async_client
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                headers=self._default_headers,
                timeout=self._timeout,
            )
        return self._async_client

    def _build_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return path

    @staticmethod
    def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
        if params is None:
            return None
        return {k: v for k, v in params.items() if v is not None}

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        files: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make a synchronous HTTP request and return parsed JSON."""
        client = self._get_client()
        url = self._build_url(path)
        response = client.request(
            method,
            url,
            json=json,
            files=files,
            params=self._clean_params(params),
        )
        request_id = response.headers.get("x-request-id")
        if response.status_code == 204:
            return None
        body = response.json() if response.content else None
        _raise_for_status(response.status_code, body, request_id)
        return body

    async def request_async(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        files: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make an asynchronous HTTP request and return parsed JSON."""
        client = self._get_async_client()
        url = self._build_url(path)
        response = await client.request(
            method,
            url,
            json=json,
            files=files,
            params=self._clean_params(params),
        )
        request_id = response.headers.get("x-request-id")
        if response.status_code == 204:
            return None
        body = response.json() if response.content else None
        _raise_for_status(response.status_code, body, request_id)
        return body

    def request_bytes(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Make a synchronous HTTP request and return raw bytes."""
        client = self._get_client()
        url = self._build_url(path)
        response = client.request(method, url, params=self._clean_params(params))
        request_id = response.headers.get("x-request-id")
        if response.status_code >= 400:
            body = response.json() if response.content else None
            _raise_for_status(response.status_code, body, request_id)
        return response.content

    async def request_bytes_async(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Make an asynchronous HTTP request and return raw bytes."""
        client = self._get_async_client()
        url = self._build_url(path)
        response = await client.request(method, url, params=self._clean_params(params))
        request_id = response.headers.get("x-request-id")
        if response.status_code >= 400:
            body = response.json() if response.content else None
            _raise_for_status(response.status_code, body, request_id)
        return response.content

    def close(self) -> None:
        """Close the synchronous HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    async def aclose(self) -> None:
        """Close the asynchronous HTTP client."""
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None
