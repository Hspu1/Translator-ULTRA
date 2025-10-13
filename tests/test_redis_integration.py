import pytest


@pytest.mark.anyio
async def test_redis_integration(redis_client):
    await redis_client.set("test_key", "test_value", ex=60)
    result = await redis_client.get("test_key")

    assert result == "test_value"
