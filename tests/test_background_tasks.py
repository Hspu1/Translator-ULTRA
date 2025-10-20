from unittest.mock import patch, AsyncMock

import pytest

from app import TranslationModel
from app.api.schemas import TranslatedRequest
from app.api.tasks import save_history_util, create_save_history_task


@pytest.mark.parametrize("original_text, should_save", [
    ("xd"*30, False), ("damn"*15, False), ("lmfao", True), ("cooked"*5, True)
])
@pytest.mark.anyio
async def test_length_validation(mock_db_session, original_text, should_save):
    # Нет проверки перевода - тест отвечает только за проверку валидации длины текста
    data = TranslatedRequest(user_id=123, original_text=original_text, translated_text="")
    obj = TranslationModel(user_id=123, original_word=original_text, translated_word="")

    result = await save_history_util(mock_db_session, data, obj)
    assert result is should_save


@pytest.mark.anyio
async def test_create_save_history_task_calls_broker():
    # Нет проверки перевода - тест отвечает только за проверку создания задачи
    data = TranslatedRequest(user_id=123, original_text=".", translated_text="")

    # Подмена реального брокера
    with patch('app.api.tasks.save_history.kiq', AsyncMock()) as mock_kiq:
        await create_save_history_task(data)
        mock_kiq.assert_called_once_with(data=data)
        # Проверка - создание задачи через kiq ровно один раз
