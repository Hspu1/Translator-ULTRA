from redis import RedisError, ResponseError
from redis.asyncio import Redis

from app.core.abstract import AbstractCache
from app.utils import logger


class RedisCache(AbstractCache):
    def __init__(self, redis_client: Redis, namespace: str = "translator"):
        self._redis = redis_client
        self._namespace = namespace

    def _get_safe_key(self, not_safe_key: str) -> str:
        return f"{self._namespace}:{not_safe_key}"

    async def get(self, key: str) -> str | None:
        safe_key = self._get_safe_key(not_safe_key=key)
        try:
            return await self._redis.get(safe_key)
        except ResponseError as e:
            logger.error(f"Redis GET response error for key {safe_key}: {e}")
            return None
        except RedisError as e:
            logger.error(f"Redis GET error for key {safe_key}: {e}")
            return None

    async def set(self, key: str, value: str, ex: int) -> None:
        safe_key = self._get_safe_key(not_safe_key=key)
        try:
            await self._redis.set(safe_key, value, ex=ex)
        except ResponseError as e:
            logger.error(f"Redis SET response error for key {safe_key}: {e}")
        except RedisError as e:
            logger.error(f"Redis SET error for key {safe_key}: {e}")

    async def aclose(self) -> None:
        await self._redis.aclose()


redis_client = Redis(
    host="127.0.0.1", port=6379,
    decode_responses=True, db=2
)
redis_cache = RedisCache(redis_client)
