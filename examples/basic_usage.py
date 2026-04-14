"""Basic synchronous usage of the Bavimail SDK."""

from bavimail import Bavimail, NotFoundError, iter_pages

# Initialize the client
client = Bavimail(
    api_key="YOUR_API_KEY",
)

# --- Domains ---
# List all domains
domains = client.domains.list()
for d in domains:
    print(f"{d.domain} ({d.status})")

# Create a domain
domain = client.domains.create("example.com", "AWS")
print(f"Created domain: {domain.id}")

# Get setup instructions
setup = client.domains.get_setup(domain.id)
for record in setup.dns_records:
    print(f"  {record.type} {record.name} -> {record.value}")

# Check DNS status
dns_status = client.domains.get_dns_status(domain.id)
print(f"Verified: {dns_status.overall_progress.verified}/{dns_status.overall_progress.total_records}")

# Trigger verification
domain = client.domains.verify(domain.id)
print(f"Domain status: {domain.status}")

# --- Aliases ---
alias = client.aliases.create(domain.id, "support")
print(f"Created alias: {alias.full_email}")

# --- Send an email ---
email = client.emails.send(
    alias_id=alias.id,
    to_email="recipient@example.com",
    subject="Welcome!",
    body="<h1>Hello!</h1><p>Welcome to our service.</p>",
)
print(f"Email sent: {email.id} (status: {email.status})")

# --- List inbound emails with pagination ---
for inbound in iter_pages(client.inbound_emails.list, alias_id=alias.id, page_size=25):
    print(f"  From: {inbound.from_email} | Subject: {inbound.subject}")

# --- Tags ---
tag = client.tags.create("important", color="#ff0000")
print(f"Created tag: {tag.name}")

# --- Error handling ---
try:
    client.domains.get("nonexistent-id")
except NotFoundError as e:
    print(f"Not found: {e.message} (code: {e.code})")

# Clean up
client.close()
