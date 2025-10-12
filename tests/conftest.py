from typing import AsyncGenerator

from fastapi import FastAPI
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from redis.asyncio import Redis
from taskiq import InMemoryBroker


@fixture(loop_scope="function")
def app_instance() -> FastAPI:
    """Создание нового приложения для каждого теста"""
    from app.main import create_app
    return create_app(testing=True)


@fixture(loop_scope="function")
async def async_client(app_instance) -> AsyncGenerator[AsyncClient, None]:
    """Mок HTTP клиента"""
    async with AsyncClient(
            transport=ASGITransport(app=app_instance),
            base_url="http://test"
    ) as client:
        yield client


@fixture
def anyio_backend() -> str:
    """Использование anyio для запуска корутин в pytest"""
    return 'asyncio'


@fixture(loop_scope="function")
async def broker_backend() -> AsyncGenerator[InMemoryBroker, None]:
    """Мок брокер бэкэнда"""
    test_broker = InMemoryBroker()
    await test_broker.startup()
    yield test_broker

    await test_broker.shutdown()


@fixture(scope="function")
async def redis_client():
    """Мок редис клиента"""
    client = Redis(host="localhost", port=6379, decode_responses=True, db=3)

    async with client:
        yield client
        await client.flushdb()
