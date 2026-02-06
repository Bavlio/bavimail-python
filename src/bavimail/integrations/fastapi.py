"""FastAPI integration for Bavimail webhook events."""

# NOTE: Do NOT use `from __future__ import annotations` here.
# FastAPI needs to resolve the `Request` type annotation at runtime,
# and with postponed evaluation it can't find the locally-imported class.

import asyncio
import inspect
import json
import logging
from typing import Any, Callable, Dict, List, Optional

from ..events import EventType, WebhookEvent
from ..exceptions import WebhookVerificationError
from ..webhook_verification import verify_webhook_signature

logger = logging.getLogger("bavimail.listener")


async def _dispatch_async(
    event: WebhookEvent,
    handlers: Dict[EventType, List[Callable[..., Any]]],
    on_error: Optional[Callable[[Exception, WebhookEvent], Any]],
) -> None:
    """Dispatch event to handlers in an async context."""
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


def create_webhook_router(
    *,
    handlers: Dict[EventType, List[Callable[..., Any]]],
    secret: str,
    path: str = "/webhooks",
    on_error: Optional[Callable[[Exception, WebhookEvent], Any]] = None,
) -> Any:
    """Create a FastAPI APIRouter that handles webhook delivery.

    Args:
        handlers: Mapping of event types to handler lists.
        secret: Hex-encoded HMAC secret.
        path: URL path for the endpoint.
        on_error: Callback for handler exceptions.

    Returns:
        A ``fastapi.APIRouter``.

    Raises:
        ImportError: If FastAPI is not installed.
    """
    try:
        from fastapi import APIRouter, Request
        from fastapi.responses import JSONResponse
    except ImportError:
        raise ImportError(
            "FastAPI is required for webhook_router(). "
            "Install it with: pip install bavimail[fastapi]"
        ) from None

    router = APIRouter()
    normalised = "/" + path.strip("/")

    @router.get(normalised)
    async def health_check() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @router.post(normalised)
    async def webhook_handler(request: Request) -> JSONResponse:
        body = await request.body()
        signature = request.headers.get("x-webhook-signature", "")
        timestamp = request.headers.get("x-webhook-timestamp", "")

        try:
            verify_webhook_signature(
                payload=body,
                signature=signature,
                timestamp=timestamp,
                secret=secret,
            )
        except WebhookVerificationError as exc:
            logger.warning("Webhook signature verification failed: %s", exc)
            return JSONResponse({"error": "invalid signature"}, status_code=403)

        try:
            raw = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("Failed to parse webhook JSON: %s", exc)
            return JSONResponse({"error": "invalid JSON"}, status_code=400)

        try:
            event = WebhookEvent.from_dict(raw)
        except (KeyError, ValueError) as exc:
            logger.warning("Failed to parse webhook event: %s", exc)
            return JSONResponse({"error": "invalid event payload"}, status_code=400)

        await _dispatch_async(event, handlers, on_error)
        return JSONResponse({"status": "ok"})

    return router
