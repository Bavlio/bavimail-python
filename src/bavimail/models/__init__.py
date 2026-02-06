"""Data models for the Bavimail SDK."""

from .alias import Alias
from .conversation import (
    ConversationDetail,
    ConversationMessage,
    ConversationSummary,
)
from .domain import (
    DNSRecord,
    DNSRecordWithStatus,
    DNSVerificationProgress,
    DNSVerificationResponse,
    Domain,
    DomainSetup,
    MailFromStatusInfo,
)
from .email import AttachmentMetadata, Email
from .inbound_email import (
    InboundAttachmentMetadata,
    InboundEmailDetail,
    InboundEmailSummary,
    Verdict,
)
from .tag import EmailTag, Tag, TagSummary
from .webhook import Webhook, WebhookCreated, WebhookSecret

__all__ = [
    "Alias",
    "AttachmentMetadata",
    "ConversationDetail",
    "ConversationMessage",
    "ConversationSummary",
    "DNSRecord",
    "DNSRecordWithStatus",
    "DNSVerificationProgress",
    "DNSVerificationResponse",
    "Domain",
    "DomainSetup",
    "Email",
    "EmailTag",
    "InboundAttachmentMetadata",
    "InboundEmailDetail",
    "InboundEmailSummary",
    "MailFromStatusInfo",
    "Tag",
    "TagSummary",
    "Verdict",
    "Webhook",
    "WebhookCreated",
    "WebhookSecret",
]
