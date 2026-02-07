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
from .email import (
    AttachmentMetadata,
    BatchEmailItemError,
    BatchEmailItemResult,
    BatchEmailResponse,
    Email,
    EmailClick,
    TrackedLink,
)
from .inbound_email import (
    InboundAttachmentMetadata,
    InboundEmailDetail,
    InboundEmailSummary,
    Verdict,
)
from .integration import (
    BootstrapApiKeyResponse,
    IntegrationInfo,
    RevokeApiKeyResponse,
)
from .tag import EmailTag, Tag, TagSummary
from .webhook import Webhook, WebhookCreated, WebhookSecret

__all__ = [
    "Alias",
    "AttachmentMetadata",
    "BatchEmailItemError",
    "BatchEmailItemResult",
    "BatchEmailResponse",
    "BootstrapApiKeyResponse",
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
    "EmailClick",
    "EmailTag",
    "InboundAttachmentMetadata",
    "InboundEmailDetail",
    "InboundEmailSummary",
    "IntegrationInfo",
    "MailFromStatusInfo",
    "RevokeApiKeyResponse",
    "Tag",
    "TagSummary",
    "TrackedLink",
    "Verdict",
    "Webhook",
    "WebhookCreated",
    "WebhookSecret",
]
