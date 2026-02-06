"""Tests for pagination helpers."""

from __future__ import annotations

from typing import Any

import pytest

from bavimail.pagination import iter_pages, iter_pages_async


def _make_list_method(
    pages: list[list[str]],
) -> Any:
    """Create a fake list method that returns predefined pages."""
    call_count = 0

    def method(
        limit: int = 50, offset: int = 0, **kwargs: Any
    ) -> list[str]:
        nonlocal call_count
        if call_count < len(pages):
            page = pages[call_count]
            call_count += 1
            return page
        return []

    return method


def test_iter_pages_single_page() -> None:
    method = _make_list_method([["a", "b"]])
    result = list(iter_pages(method, page_size=10))
    assert result == ["a", "b"]


def test_iter_pages_multiple_pages() -> None:
    method = _make_list_method([["a", "b"], ["c", "d"], ["e"]])
    result = list(iter_pages(method, page_size=2))
    assert result == ["a", "b", "c", "d", "e"]


def test_iter_pages_empty() -> None:
    method = _make_list_method([[]])
    result = list(iter_pages(method, page_size=10))
    assert result == []


def test_iter_pages_stops_on_short_page() -> None:
    """When a page is shorter than page_size, iteration should stop."""
    method = _make_list_method([["a", "b"], ["c"]])
    result = list(iter_pages(method, page_size=2))
    assert result == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_iter_pages_async_multiple() -> None:
    pages = [["x", "y"], ["z"]]
    call_count = 0

    async def method(
        limit: int = 50, offset: int = 0, **kwargs: Any
    ) -> list[str]:
        nonlocal call_count
        if call_count < len(pages):
            page = pages[call_count]
            call_count += 1
            return page
        return []

    result = []
    async for item in iter_pages_async(method, page_size=2):
        result.append(item)
    assert result == ["x", "y", "z"]


@pytest.mark.asyncio
async def test_iter_pages_async_empty() -> None:
    async def method(
        limit: int = 50, offset: int = 0, **kwargs: Any
    ) -> list[str]:
        return []

    result = []
    async for item in iter_pages_async(method, page_size=10):
        result.append(item)
    assert result == []
