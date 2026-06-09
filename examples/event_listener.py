"""Example: Event listener system for Bavimail webhooks.

Demonstrates four usage modes:
1. Standalone server with auto-created webhook
2. Standalone server with pre-existing webhook secret
3. Flask blueprint integration
4. FastAPI router integration
"""

from bavimail import Bavimail, EventType, WebhookEvent

client = Bavimail(api_key="YOUR_API_KEY")


# Register handlers using the @client.on() decorator
@client.on(EventType.INBOUND_RECEIVED)
def handle_inbound(event: WebhookEvent):
    print(f"New email from: {event.data['from_email']}")
    print(f"Subject: {event.data['subject']}")


@client.on([EventType.DOMAIN_VERIFIED, EventType.DOMAIN_FAILED])
def handle_domain(event: WebhookEvent):
    print(f"Domain event: {event.event_type} - {event.data['domain']}")


@client.on(EventType.OUTBOUND_FAILED)
def handle_failure(event: WebhookEvent):
    print(f"Email delivery failed: {event.data.get('error_message')}")


@client.on(EventType.WEBHOOK_TEST)
def handle_test(event: WebhookEvent):
    print("Test webhook received!")


# ---- Mode 1: Standalone with auto-created webhook --------------------------
# The SDK creates a webhook via the API, starts a server, and cleans up on exit.
#
# client.listen(port=8080, webhook_url="https://my-server.com/webhooks")


# ---- Mode 2: Standalone with pre-existing webhook --------------------------
# If you already have a webhook and its secret, skip auto-creation.
#
# client.listen(port=8080, secret="your_hex_secret_here")


# ---- Mode 3: Flask blueprint -----------------------------------------------
# from flask import Flask
#
# app = Flask(__name__)
# blueprint = client.webhook_blueprint("/webhooks", secret="your_hex_secret_here")
# app.register_blueprint(blueprint)
#
# if __name__ == "__main__":
#     app.run(port=8080)


# ---- Mode 4: FastAPI router ------------------------------------------------
# from fastapi import FastAPI
#
# app = FastAPI()
# router = client.webhook_router("/webhooks", secret="your_hex_secret_here")
# app.include_router(router)
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, port=8080)


# ---- Typed event data (optional) -------------------------------------------
# For typed access to event payloads, import the specific data model:
#
# from bavimail.events import InboundReceivedData
#
# @client.on(EventType.INBOUND_RECEIVED)
# def handle_typed(event: WebhookEvent):
#     data = InboundReceivedData.from_dict(event.data)
#     print(f"From: {data.from_email}, Subject: {data.subject}")
#     print(f"Alias: {data.alias}, Attachments: {data.attachment_count}")
