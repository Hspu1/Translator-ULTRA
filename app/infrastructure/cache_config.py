from typing import Any

from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis_client: Redis):
        self._redis = redis_client

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, expire: int) -> None:
        await self._redis.set(key, value, ex=expire)

    async def ping(self) -> bool:
        return await self._redis.ping()

    async def aclose(self) -> None:
        await self._redis.aclose()
