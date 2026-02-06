"""Flask integration for Bavimail webhook events."""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
from typing import Any, Callable, Optional

from ..events import EventType, WebhookEvent
from ..exceptions import WebhookVerificationError
from ..webhook_verification import verify_webhook_signature

logger = logging.getLogger("bavimail.listener")


def _dispatch_sync(
    event: WebhookEvent,
    handlers: dict[EventType, list[Callable[..., Any]]],
    on_error: Optional[Callable[[Exception, WebhookEvent], Any]],
) -> None:
    """Dispatch event to handlers in a sync context."""
    handler_list = handlers.get(event.event_type, [])
    for handler in handler_list:
        try:
            if inspect.iscoroutinefunction(handler):
                asyncio.run(handler(event))
            else:
                handler(event)
        except Exception as exc:
            logger.exception("Handler %r raised an exception", handler.__name__)
            if on_error is not None:
                try:
                    on_error(exc, event)
                except Exception:
                    logger.exception("on_error callback itself raised")


def create_webhook_blueprint(
    *,
    handlers: dict[EventType, list[Callable[..., Any]]],
    secret: str,
    path: str = "/webhooks",
    on_error: Optional[Callable[[Exception, WebhookEvent], Any]] = None,
) -> Any:
    """Create a Flask Blueprint that handles webhook delivery.

    Args:
        handlers: Mapping of event types to handler lists.
        secret: Hex-encoded HMAC secret.
        path: URL path for the endpoint.
        on_error: Callback for handler exceptions.

    Returns:
        A ``flask.Blueprint``.

    Raises:
        ImportError: If Flask is not installed.
    """
    try:
        from flask import Blueprint, Response, request
    except ImportError:
        raise ImportError(
            "Flask is required for webhook_blueprint(). "
            "Install it with: pip install bavimail[flask]"
        ) from None

    bp = Blueprint("bavimail_webhooks", __name__)
    # Normalise path
    normalised = "/" + path.strip("/")

    @bp.route(normalised, methods=["GET"])
    def health_check() -> Response:
        return Response(
            json.dumps({"status": "ok"}),
            status=200,
            content_type="application/json",
        )

    @bp.route(normalised, methods=["POST"])
    def webhook_handler() -> Response:
        body = request.get_data()
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
            return Response(
                json.dumps({"error": "invalid signature"}),
                status=403,
                content_type="application/json",
            )

        try:
            raw = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("Failed to parse webhook JSON: %s", exc)
            return Response(
                json.dumps({"error": "invalid JSON"}),
                status=400,
                content_type="application/json",
            )

        try:
            event = WebhookEvent.from_dict(raw)
        except (KeyError, ValueError) as exc:
            logger.warning("Failed to parse webhook event: %s", exc)
            return Response(
                json.dumps({"error": "invalid event payload"}),
                status=400,
                content_type="application/json",
            )

        _dispatch_sync(event, handlers, on_error)
        return Response(
            json.dumps({"status": "ok"}),
            status=200,
            content_type="application/json",
        )

    return bp
