from pytest import fixture
from httpx import AsyncClient, ASGITransport
from taskiq import InMemoryBroker


@fixture(scope="function")
def app_instance():
    """Создание нового приложения для каждого теста"""
    from app.main import create_app
    return create_app(testing=True)


@fixture(scope="function")
async def async_client(app_instance):
    """Mок HTTP клиента"""
    async with AsyncClient(
            transport=ASGITransport(app=app_instance),
            base_url="http://test"
    ) as client:
        yield client


@fixture
def anyio_backend():
    """Использование anyio для запуска корутин в pytest"""
    return 'asyncio'


@fixture(scope="function")
async def broker_backend():
    """Мок брокер бэкэнда"""
    test_broker = InMemoryBroker()
    await test_broker.startup()
    yield test_broker

    await test_broker.shutdown()
