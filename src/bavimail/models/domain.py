"""Domain-related data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ._base import _parse_datetime


@dataclass(frozen=True)
class DNSRecord:
    """A DNS record to configure for domain verification."""

    type: str
    name: str
    value: str
    priority: int | None = None
    ttl: int | None = 300
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DNSRecord:
        return cls(
            type=data["type"],
            name=data["name"],
            value=data["value"],
            priority=data.get("priority"),
            ttl=data.get("ttl", 300),
            description=data.get("description"),
        )


@dataclass(frozen=True)
class DNSRecordWithStatus:
    """A DNS record with its live verification status."""

    type: str
    name: str
    value: str
    status: str
    last_checked: datetime | None = None
    priority: int | None = None
    ttl: int | None = 300
    description: str | None = None
    actual_value: str | None = None
    error_message: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DNSRecordWithStatus:
        return cls(
            type=data["type"],
            name=data["name"],
            value=data["value"],
            status=data["status"],
            last_checked=_parse_datetime(data.get("last_checked")),
            priority=data.get("priority"),
            ttl=data.get("ttl", 300),
            description=data.get("description"),
            actual_value=data.get("actual_value"),
            error_message=data.get("error_message"),
        )


@dataclass(frozen=True)
class DNSVerificationProgress:
    """Overall progress of DNS record verification."""

    total_records: int
    verified: int
    not_configured: int
    incorrect: int
    errors: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DNSVerificationProgress:
        return cls(
            total_records=data["total_records"],
            verified=data["verified"],
            not_configured=data["not_configured"],
            incorrect=data["incorrect"],
            errors=data["errors"],
        )


@dataclass(frozen=True)
class MailFromStatusInfo:
    """MAIL FROM domain configuration status."""

    status: str
    message: str
    mail_from_domain: str | None = None
    error: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MailFromStatusInfo:
        return cls(
            status=data["status"],
            message=data["message"],
            mail_from_domain=data.get("mail_from_domain"),
            error=data.get("error"),
        )


@dataclass(frozen=True)
class DNSVerificationResponse:
    """Full DNS verification response with per-record status."""

    domain: str
    overall_progress: DNSVerificationProgress
    records: list[DNSRecordWithStatus]
    last_checked: datetime | None = None
    mail_from_status: MailFromStatusInfo | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DNSVerificationResponse:
        return cls(
            domain=data["domain"],
            overall_progress=DNSVerificationProgress.from_dict(data["overall_progress"]),
            records=[DNSRecordWithStatus.from_dict(r) for r in data["records"]],
            last_checked=_parse_datetime(data.get("last_checked")),
            mail_from_status=(
                MailFromStatusInfo.from_dict(data["mail_from_status"])
                if data.get("mail_from_status")
                else None
            ),
        )


@dataclass(frozen=True)
class DomainSetup:
    """DNS setup instructions for a domain."""

    domain: str
    dns_records: list[DNSRecord]
    verification_instructions: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainSetup:
        return cls(
            domain=data["domain"],
            dns_records=[DNSRecord.from_dict(r) for r in data["dns_records"]],
            verification_instructions=data["verification_instructions"],
        )


@dataclass(frozen=True)
class Domain:
    """A domain registered with Bavimail.

    Attributes:
        id: Unique identifier for the domain.
        domain: Domain name (e.g., "example.com").
        status: Verification status: "provisioning", "pending", "verifying",
            "verified", or "failed".
        created_at: When the domain was created.
        updated_at: When the domain was last updated.
        inbound_enabled: Whether inbound email is enabled for this domain.
        verified_at: When the domain was successfully verified.
        verification_error: Error message from the last failed verification.
        strip_tracking_on_read: Whether to remove tracking pixels when reading emails.
        extra_retained_headers: Additional heavy headers retained beyond the default set.
        retained_headers: Effective stored header patterns for inbound emails.
    """

    id: str
    domain: str
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    inbound_enabled: bool = True
    verified_at: datetime | None = None
    verification_error: str | None = None
    strip_tracking_on_read: bool = False
    extra_retained_headers: list[str] | None = None
    retained_headers: list[str] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Domain:
        return cls(
            id=str(data["id"]),
            domain=data["domain"],
            status=data["status"],
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            inbound_enabled=data.get("inbound_enabled", True),
            verified_at=_parse_datetime(data.get("verified_at")),
            verification_error=data.get("verification_error"),
            strip_tracking_on_read=data.get("strip_tracking_on_read", False),
            extra_retained_headers=data.get("extra_retained_headers"),
            retained_headers=data.get("retained_headers"),
        )
