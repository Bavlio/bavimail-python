"""Bavimail Python SDK."""

from ._client import Bavimail
from ._version import __version__
from .events import EventType, WebhookEvent
from .exceptions import (
    APIError,
    AuthenticationError,
    BavimailError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ProviderError,
    RateLimitError,
    ValidationError,
    WebhookVerificationError,
)
from .models import (
    Alias,
    AttachmentMetadata,
    ConversationDetail,
    ConversationMessage,
    ConversationSummary,
    DNSRecord,
    DNSRecordWithStatus,
    DNSVerificationProgress,
    DNSVerificationResponse,
    Domain,
    DomainSetup,
    Email,
    EmailTag,
    InboundAttachmentMetadata,
    InboundEmailDetail,
    InboundEmailSummary,
    MailFromStatusInfo,
    Tag,
    TagSummary,
    Verdict,
    Webhook,
    WebhookCreated,
    WebhookSecret,
)
from .pagination import iter_pages, iter_pages_async
from .webhook_verification import verify_webhook_signature

__all__ = [
    # Client
    "Bavimail",
    # Version
    "__version__",
    # Exceptions
    "APIError",
    "AuthenticationError",
    "BavimailError",
    "ConflictError",
    "ForbiddenError",
    "InternalServerError",
    "NotFoundError",
    "ProviderError",
    "RateLimitError",
    "ValidationError",
    "WebhookVerificationError",
    # Models
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
    # Events
    "EventType",
    "WebhookEvent",
    # Utilities
    "iter_pages",
    "iter_pages_async",
    "verify_webhook_signature",
]
