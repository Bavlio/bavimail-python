"""Sentinel type for distinguishing 'not provided' from None in update methods."""

from __future__ import annotations

from typing import TypeVar, Union


class _UnsetType:
    """Sentinel singleton to distinguish 'not provided' from None."""

    _instance: _UnsetType | None = None

    def __new__(cls) -> _UnsetType:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSET"

    def __bool__(self) -> bool:
        return False


UNSET = _UnsetType()
"""Sentinel value meaning 'parameter was not provided'.

Use this to distinguish between a parameter not being passed
(keep current value) and explicitly passing None (clear the value).
"""

# Type variable for generic Omittable type
T = TypeVar("T")

# Type alias for optional update parameters that can be omitted
Omittable = Union[T, _UnsetType]
