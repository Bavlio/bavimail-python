"""Pagination helpers for iterating over list endpoints."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def iter_pages(
    method: Callable[..., list[T]],
    *,
    page_size: int = 50,
    **kwargs: Any,
) -> Iterator[T]:
    """Iterate over all pages of a paginated list endpoint (sync).

    Example::

        for email in iter_pages(client.inbound_emails.list, alias_id="..."):
            print(email.subject)

    Args:
        method: A sync list method (e.g. ``client.inbound_emails.list``).
        page_size: Number of items per page (default 50).
        **kwargs: Additional keyword arguments passed to the list method.

    Yields:
        Individual items from each page.
    """
    offset = kwargs.pop("offset", 0)
    while True:
        page = method(limit=page_size, offset=offset, **kwargs)
        if not page:
            break
        yield from page
        if len(page) < page_size:
            break
        offset += len(page)


async def iter_pages_async(
    method: Callable[..., Any],
    *,
    page_size: int = 50,
    **kwargs: Any,
) -> AsyncIterator[T]:
    """Iterate over all pages of a paginated list endpoint (async).

    Example::

        async for email in iter_pages_async(client.inbound_emails.list_async):
            print(email.subject)

    Args:
        method: An async list method (e.g. ``client.inbound_emails.list_async``).
        page_size: Number of items per page (default 50).
        **kwargs: Additional keyword arguments passed to the list method.

    Yields:
        Individual items from each page.
    """
    offset = kwargs.pop("offset", 0)
    while True:
        page = await method(limit=page_size, offset=offset, **kwargs)
        if not page:
            break
        for item in page:
            yield item
        if len(page) < page_size:
            break
        offset += len(page)
