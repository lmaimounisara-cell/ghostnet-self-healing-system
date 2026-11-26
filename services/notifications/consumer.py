import asyncio
import json
import os

import aio_pika


seen_message_ids: set[str] = set()


async def handle_message(message):
    async with message.process():
        event = json.loads(message.body)

        message_id = event.get("message_id") or message.message_id

        if message_id and message_id in seen_message_ids:
            print(f"Duplicate ignored: {message_id}", flush=True)
            return

        email = event.get("email")

        if email:
            print(
                f"Notification envoyee : job #{event['job_id']} -> {email}",
                flush=True
            )
        else:
            print(
                f"Legacy event: job #{event['job_id']} has no email",
                flush=True
            )

        if message_id:
            seen_message_ids.add(message_id)


async def main():
    connection = await aio_pika.connect_robust(
        os.environ["AMQP_URL"],
        fail_fast=False
    )

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        queue = await channel.declare_queue(
            "notifications",
            durable=True
        )

        await queue.bind(
            exchange,
            routing_key="job.created"
        )

        await queue.consume(handle_message)

        print("Notifications service ready", flush=True)

        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())