from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from redis.asyncio import Redis
from taskiq import InMemoryBroker
from fakeredis import FakeAsyncRedis


@fixture(loop_scope="function")
def app_instance() -> FastAPI:
    """Создание нового приложения для каждого теста"""
    from app.main import create_app
    return create_app(testing=True)


@fixture(loop_scope="function")
async def mock_async_client(app_instance) -> AsyncGenerator[AsyncClient, None]:
    """Mок HTTP клиента"""
    async with AsyncClient(
            transport=ASGITransport(app=app_instance),
            base_url="http://test"
    ) as client:
        yield client


@fixture
def anyio_backend() -> str:
    """Использование anyio для запуска
    корутин в pytest (рекомендация в доке)"""
    return 'asyncio'


@fixture(loop_scope="function")
async def mock_broker_backend() -> AsyncGenerator[InMemoryBroker, None]:
    """Мок брокер бэкэнда"""
    test_broker = InMemoryBroker(await_inplace=True)
    await test_broker.startup()
    yield test_broker
    await test_broker.shutdown()


@fixture(scope="function")
async def redis_client():
    """Тестовый редис клиент (базовая проверка интеграции)"""
    client = Redis(host="localhost", port=6379, decode_responses=True, db=3)
    async with client:
        yield client
        await client.flushdb()


@fixture(scope="function")
async def fake_redis():
    """Фейковый редис клиент (модульное тестирование)"""
    redis = FakeAsyncRedis(decode_responses=True)
    yield redis
    await redis.flushall()


@fixture(scope="function")
def mock_redis_request(fake_redis):
    """Мок запроса в редис"""
    mock_request = AsyncMock()
    mock_request.app.state.redis_cache = fake_redis
    return mock_request


@fixture(scope="function")
def mock_db_session():
    """Мок асинхронной сессии БД"""
    session = MagicMock()
    session.begin.return_value.__aenter__ = AsyncMock(return_value=None)
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    # Пустышка с асинк входом и выходом ->

    return session


@fixture(scope="function")
def mock_async_session_maker(mock_db_session):
    """Мок async_session_maker"""
    mock = AsyncMock(return_value=mock_db_session)
    return mock
