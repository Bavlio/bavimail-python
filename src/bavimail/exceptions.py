"""Exception hierarchy for the Bavimail SDK."""

from __future__ import annotations

from typing import Any


class BavimailError(Exception):
    """Base exception for all Bavimail SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(BavimailError):
    """Error returned by the Bavimail API.

    Attributes:
        status_code: HTTP status code.
        code: Machine-readable error code (e.g. ``DOMAIN_NOT_FOUND``).
        category: Error category (e.g. ``not_found``, ``validation``).
        context: Additional context from the API.
        request_id: Request ID for debugging.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: str | None = None,
        category: str | None = None,
        context: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.category = category
        self.context = context
        self.request_id = request_id
        super().__init__(message)

    def __repr__(self) -> str:
        parts = [f"status_code={self.status_code}"]
        if self.code:
            parts.append(f"code={self.code!r}")
        if self.category:
            parts.append(f"category={self.category!r}")
        return f"APIError({', '.join(parts)}, message={self.message!r})"


class NotFoundError(APIError):
    """Resource not found (404)."""


class ValidationError(APIError):
    """Validation error (400)."""


class ConflictError(APIError):
    """Resource conflict (409)."""


class AuthenticationError(APIError):
    """Authentication failed (401)."""


class ForbiddenError(APIError):
    """Permission denied (403)."""


class RateLimitError(APIError):
    """Rate limit exceeded (429)."""


class ProviderError(APIError):
    """External provider error (502/503)."""


class InternalServerError(APIError):
    """Internal server error (500)."""


class WebhookVerificationError(BavimailError):
    """Webhook signature verification failed."""


_STATUS_TO_EXCEPTION: dict[int, type] = {
    400: ValidationError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
    500: InternalServerError,
    502: ProviderError,
    503: ProviderError,
}


def _raise_for_status(
    status_code: int,
    body: Any,
    request_id: str | None = None,
) -> None:
    """Parse API error response and raise the appropriate exception.

    Handles both structured and simple error formats:
    - Structured: ``{"detail": {"message": "...", "code": "...", "category": "..."}}``
    - Simple: ``{"detail": "string message"}``
    """
    if 200 <= status_code < 300:
        return

    message = f"API error (HTTP {status_code})"
    code: str | None = None
    category: str | None = None
    context: dict[str, Any] | None = None

    if isinstance(body, dict):
        detail = body.get("detail")
        if isinstance(detail, dict):
            message = detail.get("message", message)
            code = detail.get("code")
            category = detail.get("category")
            context = detail.get("context")
        elif isinstance(detail, str):
            message = detail
        elif isinstance(body.get("error"), str):
            message = body["error"]
            if body.get("detail"):
                message = f"{message}: {body['detail']}"

    exc_cls = _STATUS_TO_EXCEPTION.get(status_code, APIError)

    raise exc_cls(
        message,
        status_code=status_code,
        code=code,
        category=category,
        context=context,
        request_id=request_id,
    )
