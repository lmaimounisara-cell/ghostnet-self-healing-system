import asyncio
import json
import os

import aio_pika


seen_message_ids: set[str] = set()


async def handle_message(message):
    async with message.process():
        message_id = message.message_id
        if message_id and message_id in seen_message_ids:
            return

        event = json.loads(message.body)
        print(f"Notification: job #{event['job_id']} was created", flush=True)

        if message_id:
            seen_message_ids.add(message_id)


async def main():
    connection = await aio_pika.connect_robust(os.environ["AMQP_URL"])
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            "events", aio_pika.ExchangeType.TOPIC, durable=True
        )
        queue = await channel.declare_queue("notifications", durable=True)
        await queue.bind(exchange, routing_key="job.created")
        await queue.consume(handle_message)
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())