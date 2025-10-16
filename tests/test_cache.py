from unittest.mock import AsyncMock

import pytest

from app.api.routs_logic import translator_logic
from app.api.schemas import TranslatedRequest


@pytest.mark.anyio
async def test_cache1(fake_redis, mock_redis_request):
    fake_key = "translate:1:Hello"
    await fake_redis.set(fake_key, "Привет")
    fake_data = TranslatedRequest(user_id=1, original_text="Hello")
    result = await translator_logic(fake_data, mock_redis_request)

    assert result["cached"] is True
    assert result["translated_text"] == "Привет"
