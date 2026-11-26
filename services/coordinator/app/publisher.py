import asyncio
import json
import os
from uuid import uuid4

import aio_pika


async def publish_job_created(job_id: int, email: str) -> None:
    async with asyncio.timeout(2):
        connection = await aio_pika.connect(os.environ["AMQP_URL"])

        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange(
                "events",
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )

            message_id = str(uuid4())

            message = aio_pika.Message(
                body=json.dumps({
                    "message_id": message_id,
                    "job_id": job_id,
                    "email": email
                }).encode("utf-8"),
                content_type="application/json",
                message_id=message_id,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            await exchange.publish(
                message,
                routing_key="job.created"
            )