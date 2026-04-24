"""Main Bavimail client."""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, Callable

import httpx

from ._http import HttpClient
from .events import EventType, WebhookEvent
from .resources.aliases import Aliases
from .resources.analytics import Analytics
from .resources.attachments import Attachments
from .resources.conversations import Conversations
from .resources.domains import Domains
from .resources.emails import Emails
from .resources.inbound_emails import InboundEmails
from .resources.inbox import Inbox
from .resources.suppressions import Suppressions
from .resources.tags import Tags
from .resources.webhooks import Webhooks

logger = logging.getLogger("bavimail.listener")

_List = list  # alias to avoid shadowing


class Bavimail:
    """Client for the Bavimail API.

    Provides both synchronous and asynchronous access to all API resources.
    Async methods have an ``_async`` suffix.

    Example (sync)::

        client = Bavimail(api_key="YOUR_API_KEY")
        domains = client.domains.list()

    Example (async)::

        async with Bavimail(api_key="YOUR_API_KEY") as client:
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
        self.attachments = Attachments(self._http)
        self.analytics = Analytics(self._http)
        self.emails = Emails(self._http)
        self.inbound_emails = InboundEmails(self._http)
        self.inbox = Inbox(self._http)
        self.conversations = Conversations(self._http)
        self.suppressions = Suppressions(self._http)
        self.tags = Tags(self._http)
        self.webhooks = Webhooks(self._http)
        self._handlers: dict[EventType, _List[Callable[..., Any]]] = {}

    # -- Event registration ---------------------------------------------------

    def on(
        self,
        event_type: EventType | _List[EventType],
    ) -> Callable[..., Any]:
        """Register a handler for one or more event types.

        Can be used as a decorator::

            @client.on(EventType.INBOUND_RECEIVED)
            def handle(event: WebhookEvent):
                ...

            @client.on([EventType.DOMAIN_VERIFIED, EventType.DOMAIN_FAILED])
            def handle_domain(event: WebhookEvent):
                ...

        Works with both sync and async functions.
        """
        types = event_type if isinstance(event_type, list) else [event_type]

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            for et in types:
                self._handlers.setdefault(et, []).append(func)
            return func

        return decorator

    # -- Standalone server ----------------------------------------------------

    def listen(
        self,
        *,
        port: int = 8000,
        host: str = "0.0.0.0",
        webhook_path: str = "/webhooks",
        webhook_url: str | None = None,
        secret: str | None = None,
        description: str | None = None,
        cleanup: bool = True,
        log_level: str = "info",
        on_error: Callable[[Exception, WebhookEvent], Any] | None = None,
    ) -> None:
        """Start a standalone webhook server (blocking).

        Two modes:

        **Auto-create** (no *secret*): Requires *webhook_url*. Creates a
        webhook via the API using the event types from registered handlers,
        starts the server, and deletes the webhook on shutdown when
        *cleanup* is ``True``.

        **Pre-existing** (*secret* provided): No API calls - just starts the
        server with the given secret.

        Args:
            port: Port to bind (default 8000).
            host: Host to bind (default ``0.0.0.0``).
            webhook_path: URL path for the webhook endpoint.
            webhook_url: Public URL for auto-creating a webhook.
            secret: Hex-encoded HMAC secret (skip auto-creation).
            description: Description for the auto-created webhook.
            cleanup: Delete the auto-created webhook on shutdown.
            log_level: Uvicorn log level.
            on_error: Callback for handler exceptions.

        Raises:
            ValueError: If no handlers are registered or neither
                *webhook_url* nor *secret* is provided.
            ImportError: If ``uvicorn`` is not installed.
        """
        try:
            import uvicorn
        except ImportError:
            raise ImportError(
                "uvicorn is required for listen(). Install it with: pip install bavimail[listener]"
            ) from None

        if not self._handlers:
            raise ValueError("No event handlers registered. Use @client.on() first.")
        if secret is None and webhook_url is None:
            raise ValueError(
                "Provide either 'webhook_url' (auto-create) or 'secret' (pre-existing)."
            )

        from ._listener import WebhookApp

        webhook_id: str | None = None

        try:
            if secret is None:
                # Auto-create mode
                assert webhook_url is not None
                event_types = [et.value for et in self._handlers]
                result = self.webhooks.create(
                    webhook_url,
                    event_types,
                    description=description,
                )
                secret = result.secret
                webhook_id = result.id
                logger.info("Created webhook %s for %s", webhook_id, webhook_url)

            app = WebhookApp(
                handlers=self._handlers,
                secret=secret,
                path=webhook_path,
                on_error=on_error,
            )
            config = uvicorn.Config(
                app,
                host=host,
                port=port,
                log_level=log_level,
            )
            server = uvicorn.Server(config)
            server.run()
        finally:
            if cleanup and webhook_id is not None:
                try:
                    self.webhooks.delete(webhook_id)
                    logger.info("Cleaned up webhook %s", webhook_id)
                except Exception:
                    logger.exception("Failed to clean up webhook %s", webhook_id)

    async def listen_async(
        self,
        *,
        port: int = 8000,
        host: str = "0.0.0.0",
        webhook_path: str = "/webhooks",
        webhook_url: str | None = None,
        secret: str | None = None,
        description: str | None = None,
        cleanup: bool = True,
        log_level: str = "info",
        on_error: Callable[[Exception, WebhookEvent], Any] | None = None,
    ) -> None:
        """Start a standalone webhook server (async).

        Same as :meth:`listen` but for use in an async context. Uses
        ``uvicorn.Server.serve()`` instead of ``server.run()``.
        """
        try:
            import uvicorn
        except ImportError:
            raise ImportError(
                "uvicorn is required for listen_async(). "
                "Install it with: pip install bavimail[listener]"
            ) from None

        if not self._handlers:
            raise ValueError("No event handlers registered. Use @client.on() first.")
        if secret is None and webhook_url is None:
            raise ValueError(
                "Provide either 'webhook_url' (auto-create) or 'secret' (pre-existing)."
            )

        from ._listener import WebhookApp

        webhook_id: str | None = None

        try:
            if secret is None:
                assert webhook_url is not None
                event_types = [et.value for et in self._handlers]
                result = await self.webhooks.create_async(
                    webhook_url,
                    event_types,
                    description=description,
                )
                secret = result.secret
                webhook_id = result.id
                logger.info("Created webhook %s for %s", webhook_id, webhook_url)

            app = WebhookApp(
                handlers=self._handlers,
                secret=secret,
                path=webhook_path,
                on_error=on_error,
            )
            config = uvicorn.Config(
                app,
                host=host,
                port=port,
                log_level=log_level,
            )
            server = uvicorn.Server(config)
            await server.serve()
        finally:
            if cleanup and webhook_id is not None:
                try:
                    await self.webhooks.delete_async(webhook_id)
                    logger.info("Cleaned up webhook %s", webhook_id)
                except Exception:
                    logger.exception("Failed to clean up webhook %s", webhook_id)

    # -- Framework integrations -----------------------------------------------

    def webhook_blueprint(
        self,
        path: str = "/webhooks",
        *,
        secret: str,
        on_error: Callable[[Exception, WebhookEvent], Any] | None = None,
    ) -> Any:
        """Create a Flask Blueprint for receiving webhooks.

        Args:
            path: URL path for the webhook endpoint.
            secret: Hex-encoded HMAC secret (required).
            on_error: Callback for handler exceptions.

        Returns:
            A ``flask.Blueprint`` instance.

        Raises:
            ImportError: If ``flask`` is not installed.
        """
        from .integrations.flask import create_webhook_blueprint

        return create_webhook_blueprint(
            handlers=self._handlers,
            secret=secret,
            path=path,
            on_error=on_error,
        )

    def webhook_router(
        self,
        path: str = "/webhooks",
        *,
        secret: str,
        on_error: Callable[[Exception, WebhookEvent], Any] | None = None,
    ) -> Any:
        """Create a FastAPI APIRouter for receiving webhooks.

        Args:
            path: URL path for the webhook endpoint.
            secret: Hex-encoded HMAC secret (required).
            on_error: Callback for handler exceptions.

        Returns:
            A ``fastapi.APIRouter`` instance.

        Raises:
            ImportError: If ``fastapi`` is not installed.
        """
        from .integrations.fastapi import create_webhook_router

        return create_webhook_router(
            handlers=self._handlers,
            secret=secret,
            path=path,
            on_error=on_error,
        )

    # -- Lifecycle ------------------------------------------------------------

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
