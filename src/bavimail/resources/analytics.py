"""Analytics resource."""

from __future__ import annotations

from typing import Any

from ..models.analytics import (
    DeliverabilityRecent,
    DeliverabilitySummary,
    DeliverabilityTimeseries,
)
from ._base import BaseResource


class Analytics(BaseResource):
    def deliverability_summary(
        self,
        *,
        range: str | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilitySummary:
        params: dict[str, Any] = {
            "range": range,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = self._http.request("GET", "/analytics/deliverability/summary", params=params)
        return DeliverabilitySummary.from_dict(data)

    async def deliverability_summary_async(
        self,
        *,
        range: str | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilitySummary:
        params: dict[str, Any] = {
            "range": range,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = await self._http.request_async(
            "GET", "/analytics/deliverability/summary", params=params
        )
        return DeliverabilitySummary.from_dict(data)

    def deliverability_timeseries(
        self,
        *,
        range: str | None = None,
        bucket: str | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilityTimeseries:
        params: dict[str, Any] = {
            "range": range,
            "bucket": bucket,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = self._http.request("GET", "/analytics/deliverability/timeseries", params=params)
        return DeliverabilityTimeseries.from_dict(data)

    async def deliverability_timeseries_async(
        self,
        *,
        range: str | None = None,
        bucket: str | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilityTimeseries:
        params: dict[str, Any] = {
            "range": range,
            "bucket": bucket,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = await self._http.request_async(
            "GET", "/analytics/deliverability/timeseries", params=params
        )
        return DeliverabilityTimeseries.from_dict(data)

    def deliverability_recent(
        self,
        *,
        limit: int | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilityRecent:
        params: dict[str, Any] = {
            "limit": limit,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = self._http.request("GET", "/analytics/deliverability/recent", params=params)
        return DeliverabilityRecent.from_dict(data)

    async def deliverability_recent_async(
        self,
        *,
        limit: int | None = None,
        alias_id: str | None = None,
        domain_id: str | None = None,
    ) -> DeliverabilityRecent:
        params: dict[str, Any] = {
            "limit": limit,
            "alias_id": alias_id,
            "domain_id": domain_id,
        }
        data = await self._http.request_async(
            "GET", "/analytics/deliverability/recent", params=params
        )
        return DeliverabilityRecent.from_dict(data)
