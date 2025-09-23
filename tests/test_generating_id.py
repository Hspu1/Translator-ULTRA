import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_generating_id(async_client: AsyncClient) -> None:
    response = await async_client.post("/generate_user_id")
    response_data = response.json()

    assert response.status_code == 201
    assert isinstance(response_data["user_id"], int)
    assert response_data["user_id"] > 0
