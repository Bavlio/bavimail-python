"""Tests for exception parsing and hierarchy."""

from __future__ import annotations

import pytest

from bavimail.exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ProviderError,
    RateLimitError,
    ValidationError,
    _raise_for_status,
)


def test_structured_error_parsing() -> None:
    body = {
        "detail": {
            "message": "Domain not found",
            "code": "DOMAIN_NOT_FOUND",
            "category": "not_found",
            "context": {"domain_id": "abc"},
        }
    }
    with pytest.raises(NotFoundError) as exc_info:
        _raise_for_status(404, body, "req-123")
    err = exc_info.value
    assert err.message == "Domain not found"
    assert err.code == "DOMAIN_NOT_FOUND"
    assert err.category == "not_found"
    assert err.context == {"domain_id": "abc"}
    assert err.request_id == "req-123"
    assert err.status_code == 404


def test_simple_string_error() -> None:
    body = {"detail": "Something went wrong"}
    with pytest.raises(InternalServerError) as exc_info:
        _raise_for_status(500, body)
    assert exc_info.value.message == "Something went wrong"


def test_400_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        _raise_for_status(400, {"detail": {"message": "Bad input"}})


def test_401_raises_authentication_error() -> None:
    with pytest.raises(AuthenticationError):
        _raise_for_status(401, {"detail": "Unauthorized"})


def test_403_raises_forbidden_error() -> None:
    with pytest.raises(ForbiddenError):
        _raise_for_status(403, {"detail": "Forbidden"})


def test_409_raises_conflict_error() -> None:
    with pytest.raises(ConflictError):
        _raise_for_status(409, {"detail": {"message": "Already exists"}})


def test_429_raises_rate_limit_error() -> None:
    with pytest.raises(RateLimitError):
        _raise_for_status(429, {"detail": "Rate limited"})


def test_502_raises_provider_error() -> None:
    with pytest.raises(ProviderError):
        _raise_for_status(502, {"detail": "Bad gateway"})


def test_503_raises_provider_error() -> None:
    with pytest.raises(ProviderError):
        _raise_for_status(503, {"detail": "Unavailable"})


def test_unknown_status_raises_api_error() -> None:
    with pytest.raises(APIError):
        _raise_for_status(418, {"detail": "I'm a teapot"})


def test_2xx_does_not_raise() -> None:
    _raise_for_status(200, {"data": "ok"})
    _raise_for_status(201, {"data": "created"})
    _raise_for_status(204, None)


def test_error_response_format() -> None:
    body = {"error": "Not Found", "detail": "extra info"}
    with pytest.raises(NotFoundError) as exc_info:
        _raise_for_status(404, body)
    # When "detail" is a string, it's used as the message
    assert exc_info.value.message == "extra info"


def test_api_error_repr() -> None:
    err = APIError(
        "test",
        status_code=400,
        code="TEST_CODE",
        category="validation",
    )
    assert "status_code=400" in repr(err)
    assert "TEST_CODE" in repr(err)
