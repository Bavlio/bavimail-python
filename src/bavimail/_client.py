"""Main Bavimail client."""

from __future__ import annotations

from types import TracebackType

import httpx

from ._http import HttpClient
from .resources.aliases import Aliases
from .resources.conversations import Conversations
from .resources.domains import Domains
from .resources.emails import Emails
from .resources.inbound_emails import InboundEmails
from .resources.tags import Tags
from .resources.webhooks import Webhooks


class Bavimail:
    """Client for the Bavimail API.

    Provides both synchronous and asynchronous access to all API resources.
    Async methods have an ``_async`` suffix.

    Example (sync)::

        client = Bavimail(api_key="bvm_...")
        domains = client.domains.list()

    Example (async)::

        async with Bavimail(api_key="bvm_...") as client:
            domains = await client.domains.list_async()

    Args:
        api_key: Your Bavimail API key.
        base_url: Base URL of the Bavimail API (default ``https://api.bavimail.com``).
        timeout: Request timeout in seconds (default 30).
        http_client: Optional custom ``httpx.Client`` for sync requests.
        async_http_client: Optional custom ``httpx.AsyncClient`` for async requests.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.bavimail.com",
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
        async_http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._http = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            http_client=http_client,
            async_http_client=async_http_client,
        )
        self.domains = Domains(self._http)
        self.aliases = Aliases(self._http)
        self.emails = Emails(self._http)
        self.inbound_emails = InboundEmails(self._http)
        self.conversations = Conversations(self._http)
        self.tags = Tags(self._http)
        self.webhooks = Webhooks(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client(s)."""
        self._http.close()

    async def aclose(self) -> None:
        """Close the underlying async HTTP client."""
        await self._http.aclose()

    def __enter__(self) -> Bavimail:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> Bavimail:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()
