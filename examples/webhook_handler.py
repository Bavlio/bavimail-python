"""Example webhook handler using Flask or any WSGI framework."""

from bavimail import WebhookVerificationError, verify_webhook_signature

# Your webhook secret (from webhook creation response, store securely)
WEBHOOK_SECRET = "your_hex_encoded_secret_here"


def handle_webhook(request_body: bytes, headers: dict) -> dict:
    """Process an incoming Bavimail webhook.

    Args:
        request_body: Raw request body bytes.
        headers: Request headers dict.

    Returns:
        Response dict.
    """
    # 1. Verify signature
    try:
        verify_webhook_signature(
            payload=request_body,
            signature=headers.get("x-webhook-signature", ""),
            timestamp=headers.get("x-webhook-timestamp", ""),
            secret=WEBHOOK_SECRET,
        )
    except WebhookVerificationError as e:
        print(f"Webhook verification failed: {e}")
        return {"error": "Invalid signature"}, 403  # type: ignore[return-value]

    # 2. Parse the event
    import json

    event = json.loads(request_body)
    event_type = event.get("event_type", "")

    # 3. Handle specific events
    if event_type == "email.inbound.received":
        print(f"New inbound email from: {event['data']['from_email']}")
    elif event_type == "email.outbound.sent":
        print(f"Email delivered: {event['data']['id']}")
    elif event_type == "email.outbound.failed":
        print(f"Email failed: {event['data']['error_message']}")
    elif event_type == "domain.verified":
        print(f"Domain verified: {event['data']['domain']}")
    elif event_type == "webhook.test":
        print("Test webhook received!")
    else:
        print(f"Unknown event type: {event_type}")

    return {"status": "ok"}
