"""Tags resource."""

from __future__ import annotations

from typing import Any

from .._types import UNSET, _UnsetType
from ..models.tag import Tag
from ._base import BaseResource

_List = list  # alias to avoid shadowing by the list() method


class Tags(BaseResource):
    """Operations on tags."""

    def create(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        color: str | None = None,
        icon: str | None = None,
        sort_order: int | None = None,
        is_pinned: bool | None = None,
    ) -> Tag:
        """Create a new tag."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if type is not None:
            body["type"] = type
        if color is not None:
            body["color"] = color
        if icon is not None:
            body["icon"] = icon
        if sort_order is not None:
            body["sort_order"] = sort_order
        if is_pinned is not None:
            body["is_pinned"] = is_pinned
        data = self._http.request("POST", "/tags", json=body)
        return Tag.from_dict(data)

    async def create_async(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        color: str | None = None,
        icon: str | None = None,
        sort_order: int | None = None,
        is_pinned: bool | None = None,
    ) -> Tag:
        """Create a new tag (async)."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if type is not None:
            body["type"] = type
        if color is not None:
            body["color"] = color
        if icon is not None:
            body["icon"] = icon
        if sort_order is not None:
            body["sort_order"] = sort_order
        if is_pinned is not None:
            body["is_pinned"] = is_pinned
        data = await self._http.request_async("POST", "/tags", json=body)
        return Tag.from_dict(data)

    def list(self, *, include_hidden: bool | None = None) -> _List[Tag]:
        """List all tags."""
        params: dict[str, Any] = {}
        if include_hidden is not None:
            params["include_hidden"] = include_hidden
        data = self._http.request("GET", "/tags", params=params or None)
        return [Tag.from_dict(t) for t in data]

    async def list_async(
        self, *, include_hidden: bool | None = None
    ) -> _List[Tag]:
        """List all tags (async)."""
        params: dict[str, Any] = {}
        if include_hidden is not None:
            params["include_hidden"] = include_hidden
        data = await self._http.request_async(
            "GET", "/tags", params=params or None
        )
        return [Tag.from_dict(t) for t in data]

    def get(self, tag_id: str) -> Tag:
        """Get a tag by ID."""
        data = self._http.request("GET", f"/tags/{tag_id}")
        return Tag.from_dict(data)

    async def get_async(self, tag_id: str) -> Tag:
        """Get a tag by ID (async)."""
        data = await self._http.request_async("GET", f"/tags/{tag_id}")
        return Tag.from_dict(data)

    def update(
        self,
        tag_id: str,
        *,
        name: str | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
        type: str | _UnsetType = UNSET,
        color: str | None | _UnsetType = UNSET,
        icon: str | None | _UnsetType = UNSET,
        sort_order: int | _UnsetType = UNSET,
        is_pinned: bool | _UnsetType = UNSET,
        is_visible: bool | _UnsetType = UNSET,
    ) -> Tag:
        """Update a tag."""
        body: dict[str, Any] = {}
        if name is not UNSET:
            body["name"] = name
        if description is not UNSET:
            body["description"] = description
        if type is not UNSET:
            body["type"] = type
        if color is not UNSET:
            body["color"] = color
        if icon is not UNSET:
            body["icon"] = icon
        if sort_order is not UNSET:
            body["sort_order"] = sort_order
        if is_pinned is not UNSET:
            body["is_pinned"] = is_pinned
        if is_visible is not UNSET:
            body["is_visible"] = is_visible
        data = self._http.request("PATCH", f"/tags/{tag_id}", json=body)
        return Tag.from_dict(data)

    async def update_async(
        self,
        tag_id: str,
        *,
        name: str | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
        type: str | _UnsetType = UNSET,
        color: str | None | _UnsetType = UNSET,
        icon: str | None | _UnsetType = UNSET,
        sort_order: int | _UnsetType = UNSET,
        is_pinned: bool | _UnsetType = UNSET,
        is_visible: bool | _UnsetType = UNSET,
    ) -> Tag:
        """Update a tag (async)."""
        body: dict[str, Any] = {}
        if name is not UNSET:
            body["name"] = name
        if description is not UNSET:
            body["description"] = description
        if type is not UNSET:
            body["type"] = type
        if color is not UNSET:
            body["color"] = color
        if icon is not UNSET:
            body["icon"] = icon
        if sort_order is not UNSET:
            body["sort_order"] = sort_order
        if is_pinned is not UNSET:
            body["is_pinned"] = is_pinned
        if is_visible is not UNSET:
            body["is_visible"] = is_visible
        data = await self._http.request_async(
            "PATCH", f"/tags/{tag_id}", json=body
        )
        return Tag.from_dict(data)

    def delete(self, tag_id: str) -> None:
        """Delete a tag."""
        self._http.request("DELETE", f"/tags/{tag_id}")

    async def delete_async(self, tag_id: str) -> None:
        """Delete a tag (async)."""
        await self._http.request_async("DELETE", f"/tags/{tag_id}")
