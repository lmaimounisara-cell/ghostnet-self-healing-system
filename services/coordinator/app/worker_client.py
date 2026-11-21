import asyncio

import httpx
from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

breaker = CircuitBreaker(fail_max=5, reset_timeout=30)


@retry(
    retry=retry_if_exception_type((httpx.TransportError, TimeoutError)),
    stop=stop_after_attempt(2),
    wait=wait_fixed(0.2),
    reraise=True,
)
async def _request_capacity() -> bool:
    async with asyncio.timeout(1):
        async with httpx.AsyncClient() as client:
            response = await client.get("http://workers:8000/capacity")
            response.raise_for_status()
            return response.json()["available"]


def _check_capacity() -> bool:
    return breaker.call(lambda: asyncio.run(_request_capacity()))


async def get_worker_capacity() -> bool:
    try:
        return await asyncio.to_thread(_check_capacity)
    except CircuitBreakerError as exc:
        raise httpx.HTTPError("Workers circuit breaker is open") from exc