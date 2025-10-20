import pytest

from app.api.routs_logic import translator_logic
from app.api.schemas import TranslatedRequest


@pytest.mark.parametrize("user_id, original, expected", [
    (1, "Hello", "Привет"),
    (1, "Bye", "Пока"),
    (909, "猿も木から落ちる", "Обезьяны тоже падают с деревьев")
])
@pytest.mark.anyio
async def test_cache1(fake_redis, mock_redis_request, user_id, original, expected):
    fake_key = f"translate:{user_id}:{original}"
    await fake_redis.set(fake_key, expected)

    fake_data = TranslatedRequest(user_id=user_id, original_text=original)
    result = await translator_logic(fake_data, mock_redis_request)

    assert result["cached"] is True
    assert result["translated_text"] == expected
