from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from taskiq import InMemoryBroker


@fixture(loop_scope="function")
def app_instance():
    """Создание нового приложения для каждого теста"""
    from app.main import create_app
    return create_app(testing=True)


@fixture(loop_scope="function")
async def async_client(app_instance):
    """Mок HTTP клиента"""
    async with AsyncClient(
            transport=ASGITransport(app=app_instance),
            base_url="http://test"
    ) as client:
        yield client


@fixture
def anyio_backend():
    return 'asyncio'


@fixture
async def broker_backend():
    test_broker = InMemoryBroker()
    await test_broker.startup()
    yield test_broker

    await test_broker.shutdown()
