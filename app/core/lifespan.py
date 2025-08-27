from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure import create_redis_cache, create_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_cache = await create_redis_cache()
    broker = await create_broker()

    if not broker.is_worker_process:
        await broker.startup()

    await redis_cache.ping()
    app.state.redis_cache = redis_cache

    yield

    if not broker.is_worker_process:
        await broker.shutdown()
    await app.state.redis_cache.aclose()
