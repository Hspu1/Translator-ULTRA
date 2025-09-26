import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_showing_history(async_client: AsyncClient) -> None:
    test_cases = (23, 2, 1000, 356, 672, 724, 832,)
    for uid in test_cases:
        response = await async_client.get(
            "/show_history", params={"user_id": uid}
        )
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data["history"], list)
