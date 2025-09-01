from redis.asyncio import Redis
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from app.infrastructure.cache_config import RedisCache


def create_redis_cache() -> RedisCache:
    redis_client = Redis(
        host="127.0.0.1", port=6379,
        decode_responses=True, db=2
    )
    redis_cache = RedisCache(redis_client)

    return redis_cache


def create_redis_broker() -> RedisStreamBroker:
    backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
    broker = RedisStreamBroker(
        url="redis://localhost:6379/1"
    ).with_result_backend(result_backend=backend)

    return broker
