"""Shared helpers for model parsing."""

from __future__ import annotations

from datetime import datetime, timezone


def _parse_datetime(value: str | None) -> datetime | None:
    """Parse an ISO 8601 datetime string to a datetime object."""
    if value is None:
        return None
    # Handle Z suffix
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _parse_datetime_required(value: str) -> datetime:
    """Parse an ISO 8601 datetime string, raising if None."""
    result = _parse_datetime(value)
    if result is None:
        raise ValueError("Expected a datetime string, got None")
    return result


def _ensure_utc(dt: datetime | None) -> datetime | None:
    """Ensure a datetime is timezone-aware (default to UTC)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt
