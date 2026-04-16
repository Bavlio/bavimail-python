"""Tests for the Domains resource."""

from __future__ import annotations

import httpx
import pytest

from tests.conftest import (
    SAMPLE_DOMAIN,
    json_response,
    make_async_client,
    make_client,
    no_content_response,
)


def test_create_domain() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/domains" in str(request.url)
        body = request.content.decode()
        assert "example.com" in body
        assert "AWS" in body
        assert "inbound_enabled" in body
        return json_response(SAMPLE_DOMAIN, status_code=200)

    client = make_client("https://test.com", "key", handler)
    domain = client.domains.create("example.com", "AWS")
    assert domain.domain == "example.com"
    assert domain.status == "verified"
    client.close()


def test_list_domains() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return json_response([SAMPLE_DOMAIN])

    client = make_client("https://test.com", "key", handler)
    domains = client.domains.list()
    assert len(domains) == 1
    assert domains[0].id == SAMPLE_DOMAIN["id"]
    client.close()


def test_get_domain() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert SAMPLE_DOMAIN["id"] in str(request.url)
        return json_response(SAMPLE_DOMAIN)

    client = make_client("https://test.com", "key", handler)
    domain = client.domains.get(SAMPLE_DOMAIN["id"])
    assert domain.id == SAMPLE_DOMAIN["id"]
    client.close()


def test_get_setup() -> None:
    setup_data = {
        "domain": "example.com",
        "dns_records": [
            {"type": "TXT", "name": "_amazonses.example.com", "value": "tok123"}
        ],
        "verification_instructions": "Add these DNS records.",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/setup" in str(request.url)
        return json_response(setup_data)

    client = make_client("https://test.com", "key", handler)
    setup = client.domains.get_setup(SAMPLE_DOMAIN["id"])
    assert setup.domain == "example.com"
    assert len(setup.dns_records) == 1
    client.close()


def test_get_dns_status() -> None:
    dns_data = {
        "domain": "example.com",
        "overall_progress": {
            "total_records": 5,
            "verified": 5,
            "not_configured": 0,
            "incorrect": 0,
            "errors": 0,
        },
        "records": [],
        "last_checked": "2025-01-01T00:00:00Z",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/dns-status" in str(request.url)
        return json_response(dns_data)

    client = make_client("https://test.com", "key", handler)
    status = client.domains.get_dns_status(SAMPLE_DOMAIN["id"])
    assert status.overall_progress.verified == 5
    client.close()


def test_verify_domain() -> None:
    verified = {**SAMPLE_DOMAIN, "status": "verified"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/verify" in str(request.url)
        return json_response(verified)

    client = make_client("https://test.com", "key", handler)
    domain = client.domains.verify(SAMPLE_DOMAIN["id"])
    assert domain.status == "verified"
    client.close()


def test_update_domain() -> None:
    updated = {**SAMPLE_DOMAIN, "inbound_enabled": False}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        body = request.content.decode()
        assert "false" in body.lower()
        return json_response(updated)

    client = make_client("https://test.com", "key", handler)
    domain = client.domains.update(SAMPLE_DOMAIN["id"], inbound_enabled=False)
    assert domain.inbound_enabled is False
    client.close()


def test_delete_domain() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_client("https://test.com", "key", handler)
    client.domains.delete(SAMPLE_DOMAIN["id"])
    client.close()


# Async tests


@pytest.mark.asyncio
async def test_create_domain_async() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/domains" in str(request.url)
        body = request.content.decode()
        assert "example.com" in body
        assert "AWS" in body
        assert "inbound_enabled" in body
        return json_response(SAMPLE_DOMAIN, status_code=200)

    client = make_async_client("https://test.com", "key", handler)
    domain = await client.domains.create_async("example.com", "AWS")
    assert domain.domain == "example.com"
    assert domain.status == "verified"
    await client.aclose()


@pytest.mark.asyncio
async def test_list_domains_async() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return json_response([SAMPLE_DOMAIN])

    client = make_async_client("https://test.com", "key", handler)
    domains = await client.domains.list_async()
    assert len(domains) == 1
    assert domains[0].id == SAMPLE_DOMAIN["id"]
    await client.aclose()


@pytest.mark.asyncio
async def test_get_domain_async() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert SAMPLE_DOMAIN["id"] in str(request.url)
        return json_response(SAMPLE_DOMAIN)

    client = make_async_client("https://test.com", "key", handler)
    domain = await client.domains.get_async(SAMPLE_DOMAIN["id"])
    assert domain.id == SAMPLE_DOMAIN["id"]
    await client.aclose()


@pytest.mark.asyncio
async def test_get_setup_async() -> None:
    setup_data = {
        "domain": "example.com",
        "dns_records": [
            {"type": "TXT", "name": "_amazonses.example.com", "value": "tok123"}
        ],
        "verification_instructions": "Add these DNS records.",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/setup" in str(request.url)
        return json_response(setup_data)

    client = make_async_client("https://test.com", "key", handler)
    setup = await client.domains.get_setup_async(SAMPLE_DOMAIN["id"])
    assert setup.domain == "example.com"
    assert len(setup.dns_records) == 1
    await client.aclose()


@pytest.mark.asyncio
async def test_get_dns_status_async() -> None:
    dns_data = {
        "domain": "example.com",
        "overall_progress": {
            "total_records": 5,
            "verified": 5,
            "not_configured": 0,
            "incorrect": 0,
            "errors": 0,
        },
        "records": [],
        "last_checked": "2025-01-01T00:00:00Z",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/dns-status" in str(request.url)
        return json_response(dns_data)

    client = make_async_client("https://test.com", "key", handler)
    status = await client.domains.get_dns_status_async(SAMPLE_DOMAIN["id"])
    assert status.overall_progress.verified == 5
    await client.aclose()


@pytest.mark.asyncio
async def test_verify_domain_async() -> None:
    verified = {**SAMPLE_DOMAIN, "status": "verified"}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert "/verify" in str(request.url)
        return json_response(verified)

    client = make_async_client("https://test.com", "key", handler)
    domain = await client.domains.verify_async(SAMPLE_DOMAIN["id"])
    assert domain.status == "verified"
    await client.aclose()


@pytest.mark.asyncio
async def test_update_domain_async() -> None:
    updated = {**SAMPLE_DOMAIN, "inbound_enabled": False}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        body = request.content.decode()
        assert "false" in body.lower()
        return json_response(updated)

    client = make_async_client("https://test.com", "key", handler)
    domain = await client.domains.update_async(SAMPLE_DOMAIN["id"], inbound_enabled=False)
    assert domain.inbound_enabled is False
    await client.aclose()


@pytest.mark.asyncio
async def test_delete_domain_async() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return no_content_response()

    client = make_async_client("https://test.com", "key", handler)
    await client.domains.delete_async(SAMPLE_DOMAIN["id"])
    await client.aclose()
