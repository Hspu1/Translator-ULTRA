from typing import Any

from redis.asyncio import Redis
from taskiq_redis import RedisStreamBroker, RedisAsyncResultBackend

from .abstract import AbstractCache


class RedisCache(AbstractCache):
    def __init__(self, redis_client: Redis):
        self._redis = redis_client

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, expire: int) -> None:
        await self._redis.set(key, value, ex=expire)

    async def aclose(self) -> None:
        await self._redis.aclose()


async def create_redis_cache() -> RedisCache:
    redis_client = Redis(
        host="127.0.0.1", port=6379,
        decode_responses=True, db=2
    )
    redis_cache = RedisCache(redis_client)

    return redis_cache


async def create_broker() -> RedisStreamBroker:
    backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
    broker = RedisStreamBroker(
        url="redis://localhost:6379/1"
    ).with_result_backend(result_backend=backend)

    return broker
