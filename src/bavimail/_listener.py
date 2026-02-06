"""Raw ASGI application for receiving and dispatching webhook events.

No starlette/fastapi dependency - only requires ``uvicorn`` at runtime when
used via :meth:`Bavimail.listen`.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
from typing import Any, Callable, Optional

from .events import EventType, WebhookEvent
from .exceptions import WebhookVerificationError
from .webhook_verification import verify_webhook_signature

logger = logging.getLogger("bavimail.listener")

# ASGI type aliases
Scope = dict[str, Any]
Receive = Callable[..., Any]
Send = Callable[..., Any]


async def _dispatch_event(
    event: WebhookEvent,
    handlers: dict[EventType, list[Callable[..., Any]]],
    on_error: Optional[Callable[[Exception, WebhookEvent], Any]],
) -> None:
    """Invoke all registered handlers for *event*, catching exceptions."""
    handler_list = handlers.get(event.event_type, [])
    for handler in handler_list:
        try:
            if inspect.iscoroutinefunction(handler):
                await handler(event)
            else:
                await asyncio.to_thread(handler, event)
        except Exception as exc:
            logger.exception("Handler %r raised an exception", handler.__name__)
            if on_error is not None:
                try:
                    if inspect.iscoroutinefunction(on_error):
                        await on_error(exc, event)
                    else:
                        on_error(exc, event)
                except Exception:
                    logger.exception("on_error callback itself raised")


async def _send_response(send: Send, status: int, body: bytes) -> None:
    """Send a plain-text ASGI response."""
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                [b"content-type", b"application/json"],
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


class WebhookApp:
    """Minimal ASGI app that receives webhook POSTs and dispatches to handlers.

    Args:
        handlers: Mapping of event types to handler lists (from the client).
        secret: Hex-encoded HMAC secret for signature verification.
        path: URL path to listen on (default ``/webhooks``).
        on_error: Optional callback invoked when a handler raises.
    """

    def __init__(
        self,
        *,
        handlers: dict[EventType, list[Callable[..., Any]]],
        secret: str,
        path: str = "/webhooks",
        on_error: Optional[Callable[[Exception, WebhookEvent], Any]] = None,
    ) -> None:
        self._handlers = handlers
        self._secret = secret
        # Normalise path: ensure leading slash, strip trailing slash
        self._path = "/" + path.strip("/")
        self._on_error = on_error

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return

        path: str = scope.get("path", "/")
        method: str = scope.get("method", "GET")

        # Only handle requests to the configured path
        if path.rstrip("/") != self._path.rstrip("/"):
            await _send_response(send, 404, b'{"error":"not found"}')
            return

        if method == "GET":
            await _send_response(send, 200, b'{"status":"ok"}')
            return

        if method != "POST":
            await _send_response(send, 405, b'{"error":"method not allowed"}')
            return

        # Read the full request body
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break

        # Extract headers into a dict
        headers: dict[str, str] = {}
        for name_bytes, value_bytes in scope.get("headers", []):
            headers[name_bytes.decode("latin-1").lower()] = value_bytes.decode("latin-1")

        # Verify signature
        signature = headers.get("x-webhook-signature", "")
        timestamp = headers.get("x-webhook-timestamp", "")
        try:
            verify_webhook_signature(
                payload=body,
                signature=signature,
                timestamp=timestamp,
                secret=self._secret,
            )
        except WebhookVerificationError as exc:
            logger.warning("Webhook signature verification failed: %s", exc)
            await _send_response(send, 403, b'{"error":"invalid signature"}')
            return

        # Parse JSON
        try:
            raw = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("Failed to parse webhook JSON: %s", exc)
            await _send_response(send, 400, b'{"error":"invalid JSON"}')
            return

        # Parse event
        try:
            event = WebhookEvent.from_dict(raw)
        except (KeyError, ValueError) as exc:
            logger.warning("Failed to parse webhook event: %s", exc)
            await _send_response(send, 400, b'{"error":"invalid event payload"}')
            return

        # Dispatch - always return 200 regardless of handler success
        await _dispatch_event(event, self._handlers, self._on_error)
        await _send_response(send, 200, b'{"status":"ok"}')
