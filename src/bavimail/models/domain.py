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
        status: Verification status: "pending", "verifying", "verified", or "failed".
        is_active: Whether the domain is active and can send/receive email.
        provider_key: Email provider identifier (e.g., "AWS" for Amazon SES).
        user_id: ID of the user who owns this domain.
        created_at: When the domain was created.
        updated_at: When the domain was last updated.
        provider_config: Provider-specific configuration options.
        ses_verification_token: SES domain verification token.
        ses_dkim_tokens: SES DKIM signing tokens for email authentication.
        ses_mail_from_domain: Custom MAIL FROM domain for SES.
        ses_mail_from_status: MAIL FROM domain verification status.
        ses_mail_from_error: Error message if MAIL FROM setup failed.
        verified_at: When the domain was successfully verified.
        last_verification_attempt: When verification was last attempted.
        verification_error: Error message from the last failed verification.
        strip_tracking_on_read: Whether to remove tracking pixels when reading emails.
    """

    id: str
    domain: str
    status: str
    is_active: bool
    provider_key: str
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    provider_config: dict[str, Any] | None = None
    ses_verification_token: str | None = None
    ses_dkim_tokens: list[str] | None = None
    ses_mail_from_domain: str | None = None
    ses_mail_from_status: str | None = None
    ses_mail_from_error: str | None = None
    verified_at: datetime | None = None
    last_verification_attempt: datetime | None = None
    verification_error: str | None = None
    strip_tracking_on_read: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Domain:
        return cls(
            id=str(data["id"]),
            domain=data["domain"],
            status=data["status"],
            is_active=data["is_active"],
            provider_key=data["provider_key"],
            user_id=str(data["user_id"]),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            provider_config=data.get("provider_config"),
            ses_verification_token=data.get("ses_verification_token"),
            ses_dkim_tokens=data.get("ses_dkim_tokens"),
            ses_mail_from_domain=data.get("ses_mail_from_domain"),
            ses_mail_from_status=data.get("ses_mail_from_status"),
            ses_mail_from_error=data.get("ses_mail_from_error"),
            verified_at=_parse_datetime(data.get("verified_at")),
            last_verification_attempt=_parse_datetime(
                data.get("last_verification_attempt")
            ),
            verification_error=data.get("verification_error"),
            strip_tracking_on_read=data.get("strip_tracking_on_read", False),
        )
