"""Base class for API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import HttpClient


class BaseResource:
    """Base class that holds a reference to the HTTP client."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
