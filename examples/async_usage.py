"""Async usage of the Bavimail SDK."""

import asyncio

from bavimail import Bavimail, iter_pages_async


async def main() -> None:
    async with Bavimail(
        api_key="YOUR_API_KEY",
    ) as client:
        # List domains
        domains = await client.domains.list_async()
        for d in domains:
            print(f"{d.domain} ({d.status})")

        # Send an email
        email = await client.emails.send_async(
            alias_id="your-alias-id",
            to_email="recipient@example.com",
            subject="Hello from async!",
            body="<p>Sent asynchronously.</p>",
        )
        print(f"Sent: {email.id}")

        # Paginate through inbound emails
        async for inbound in iter_pages_async(
            client.inbound_emails.list_async, page_size=25
        ):
            print(f"  {inbound.from_email}: {inbound.subject}")

        # Conversations
        conversations = await client.conversations.list_async(limit=10)
        for conv in conversations:
            print(f"Thread: {conv.subject} ({conv.message_count} messages)")


if __name__ == "__main__":
    asyncio.run(main())
