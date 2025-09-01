from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis import ConnectionError, ResponseError, RedisError

from app.infrastructure import create_redis_cache, create_redis_broker
from app.utils import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        redis_cache = create_redis_cache()
        redis_broker = create_redis_broker()

        if not redis_broker.is_worker_process:
            await redis_broker.startup()

        app.state.redis_cache = redis_cache
        app.state.redis_broker = redis_broker

        yield

        if not redis_broker.is_worker_process:
            await redis_broker.shutdown()
        await app.state.redis_cache.aclose()

    except (ConnectionError, ResponseError) as e:
        logger.critical(f"Redis startup failed: {e}")
        raise
    except RedisError as e:
        logger.critical(f"Redis startup failed (RedisError): {e}")
        raise
