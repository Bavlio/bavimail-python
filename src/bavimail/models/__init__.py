"""Data models for the Bavimail SDK."""

from .alias import Alias
from .analytics import (
    DeliverabilityRecent,
    DeliverabilityRecentRow,
    DeliverabilitySummary,
    DeliverabilityTimeseries,
    DeliverabilityTimeseriesPoint,
)
from .attachment import AttachmentFile, AttachmentUploadFile, AttachmentUploadResponse
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
    InboundHeader,
    InboundRecipient,
    Verdict,
)
from .integration import (
    BootstrapApiKeyResponse,
    IntegrationInfo,
    RevokeApiKeyResponse,
)
from .suppression import Suppression
from .tag import EmailTag, Tag, TagSummary
from .webhook import Webhook, WebhookCreated, WebhookSecret

__all__ = [
    "Alias",
    "AttachmentFile",
    "AttachmentMetadata",
    "AttachmentUploadFile",
    "AttachmentUploadResponse",
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
    "DeliverabilityRecent",
    "DeliverabilityRecentRow",
    "DeliverabilitySummary",
    "DeliverabilityTimeseries",
    "DeliverabilityTimeseriesPoint",
    "Domain",
    "DomainSetup",
    "Email",
    "EmailClick",
    "EmailTag",
    "InboundAttachmentMetadata",
    "InboundHeader",
    "InboundEmailDetail",
    "InboundEmailSummary",
    "InboundRecipient",
    "IntegrationInfo",
    "MailFromStatusInfo",
    "RevokeApiKeyResponse",
    "Suppression",
    "Tag",
    "TagSummary",
    "TrackedLink",
    "Verdict",
    "Webhook",
    "WebhookCreated",
    "WebhookSecret",
]
