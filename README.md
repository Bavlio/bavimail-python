# bavimail-python

Python SDK for the [Bavimail](https://github.com/Bavlio/bavimail-python) email service API.

## Installation

```bash
pip install bavimail
```

## Quick Start

### Synchronous

```python
from bavimail import Bavimail

client = Bavimail(
    api_key="YOUR_API_KEY",
)

# List domains
domains = client.domains.list()
for d in domains:
    print(f"{d.domain} ({d.status})")

# Send an email
email = client.emails.send(
    alias_id="your-alias-id",
    to_email="recipient@example.com",
    subject="Hello!",
    body="<p>Welcome!</p>",
)
print(f"Sent: {email.id} (status: {email.status})")

client.close()
```

### Asynchronous

Every method has an `_async` variant. Use `async with` for automatic cleanup:

```python
import asyncio
from bavimail import Bavimail

async def main():
    async with Bavimail(
        api_key="YOUR_API_KEY",
    ) as client:
        domains = await client.domains.list_async()
        email = await client.emails.send_async(
            alias_id="your-alias-id",
            to_email="recipient@example.com",
            subject="Hello!",
            body="<p>Welcome!</p>",
        )

asyncio.run(main())
```

## Resources

### Domains

```python
# Create a domain
domain = client.domains.create("example.com", "AWS", inbound_enabled=False)

# Get setup instructions (DNS records)
setup = client.domains.get_setup(domain.id)
for record in setup.dns_records:
    print(f"{record.type} {record.name} -> {record.value}")

# Check DNS verification status
dns = client.domains.get_dns_status(domain.id)
print(f"Verified: {dns.overall_progress.verified}/{dns.overall_progress.total_records}")

# Trigger verification
domain = client.domains.verify(domain.id)

# Update domain settings
domain = client.domains.update(domain.id, inbound_enabled=True)

# Delete
client.domains.delete(domain.id)
```

### Aliases

```python
alias = client.aliases.create(domain.id, "support")
aliases = client.aliases.list(domain_id=domain.id)
client.aliases.update(alias.id, "info")
client.aliases.delete(alias.id)
```

### Emails (Outbound)

```python
email = client.emails.send(
    alias_id=alias.id,
    to_email="user@example.com",
    subject="Welcome",
    body="<h1>Hello!</h1>",
    track_opens=True,
    attachments=[{
        "filename": "doc.pdf",
        "content": "<base64-encoded-content>",
        "mime_type": "application/pdf",
    }],
)

emails = client.emails.list(alias_id=alias.id, limit=50)
email = client.emails.get(email.id)
```

### Inbound Emails

```python
# List with filters
emails = client.inbound_emails.list(alias_id=alias.id, limit=25)

# Get full detail
detail = client.inbound_emails.get(email_id)

# Download raw RFC822 email
raw = client.inbound_emails.download_raw(email_id)

# Download attachment by index
attachment = client.inbound_emails.download_attachment(email_id, 0)

# Tag management
client.inbound_emails.add_tags(email_id, ["tag-id-1", "tag-id-2"])
tags = client.inbound_emails.get_tags(email_id)
client.inbound_emails.replace_tags(email_id, ["tag-id-3"])
client.inbound_emails.remove_tag(email_id, "tag-id-3")

# Delete
client.inbound_emails.delete(email_id)
```

### Conversations

```python
conversations = client.conversations.list(limit=20)
detail = client.conversations.get(conversation_id)
for msg in detail.messages:
    print(f"[{msg.direction}] {msg.from_email}: {msg.subject}")
```

### Tags

```python
tag = client.tags.create("important", color="#ff0000", is_pinned=True)
tags = client.tags.list()
tag = client.tags.update(tag.id, name="critical")
client.tags.delete(tag.id)
```

### Webhooks

```python
# Create (returns secret, shown once!)
wh = client.webhooks.create(
    url="https://hooks.example.com/bavimail",
    event_types=["email.inbound.received", "domain.verified"],
)
print(f"Secret: {wh.secret}")  # Store this!

# Verify
wh = client.webhooks.verify(wh.id, "verification-code-from-endpoint")

# Manage
webhooks = client.webhooks.list()
client.webhooks.update(wh.id, is_active=True)
client.webhooks.test(wh.id)
secret = client.webhooks.rotate_secret(wh.id)
client.webhooks.delete(wh.id)
```

## Pagination

Use `iter_pages` / `iter_pages_async` to iterate through all results:

```python
from bavimail import iter_pages, iter_pages_async

# Sync
for email in iter_pages(client.inbound_emails.list, alias_id="...", page_size=25):
    print(email.subject)

# Async
async for email in iter_pages_async(client.inbound_emails.list_async, page_size=25):
    print(email.subject)
```

## Webhook Signature Verification

Verify incoming webhook signatures in your handler:

```python
from bavimail import verify_webhook_signature, WebhookVerificationError

try:
    verify_webhook_signature(
        payload=request.body,
        signature=request.headers["x-webhook-signature"],
        timestamp=request.headers["x-webhook-timestamp"],
        secret="your-hex-secret",
    )
except WebhookVerificationError as e:
    print(f"Invalid webhook: {e}")
```

## Error Handling

All API errors raise typed exceptions:

```python
from bavimail import (
    NotFoundError,
    ValidationError,
    ConflictError,
    AuthenticationError,
    RateLimitError,
    APIError,
)

try:
    client.domains.get("nonexistent")
except NotFoundError as e:
    print(f"Not found: {e.message}")
    print(f"Error code: {e.code}")       # e.g. "DOMAIN_NOT_FOUND"
    print(f"Category: {e.category}")      # e.g. "not_found"
    print(f"Request ID: {e.request_id}")  # For debugging
    print(f"Context: {e.context}")        # e.g. {"field": "domain_id", "value": "nonexistent"}
except APIError as e:
    print(f"API error ({e.status_code}): {e.message}")
```

## Custom HTTP Client

Pass a custom `httpx.Client` for advanced configuration (proxies, custom TLS, retries):

```python
import httpx

custom = httpx.Client(
    transport=httpx.HTTPTransport(retries=3),
    timeout=60.0,
)

client = Bavimail(
    api_key="YOUR_API_KEY",
    http_client=custom,
)
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Type check
mypy src/bavimail --strict

# Lint
ruff check src/ tests/
```

## License

MIT
