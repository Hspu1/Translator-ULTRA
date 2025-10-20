from unittest.mock import patch, AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app import TranslationModel
from app.api.schemas import TranslatedRequest
from app.api.tasks import save_history_util, create_save_history_task


@pytest.mark.parametrize("original_text, should_save", [
    ("x", True), ("x"*34, True), ("x"*35, True), ("x"*36, False), ("x"*100, False)
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


@pytest.mark.anyio
async def test_save_history_util_integrity_error(mock_db_session):
    """Текста не важны - специально передаем IntegrityError в save_history_util
    не смотря ни на что -> хотим проверить результат после выброса иселючения"""
    data = TranslatedRequest(user_id=123, original_text=".", translated_text="")
    obj = TranslationModel(user_id=123, original_word=".", translated_word="")

    mock_db_session.add.side_effect = IntegrityError("Duplicate entry", {}, BaseException())

    result = await save_history_util(mock_db_session, data, obj)
    assert result is False
    mock_db_session.begin.assert_called_once()
