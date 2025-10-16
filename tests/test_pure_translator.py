import pytest

from app.api.routs_logic import translated_async
from app.api.schemas import TranslatedRequest


@pytest.mark.anyio
async def test_pure_translator():
    request_texts, response_texts = (
        "Hello World", "Le vent souffle fort ce soir", "La vida es un carnaval",
        "Die Zeit heilt alle Wunden", "猿も木から落ちる", "千里之行，始于足下",
        "الصبر مفتاح الفرج", "Il buongiorno si vede dal mattino"
    ), (
        "Привет, мир", "Сегодня вечером ветер дует сильно",
        "жизнь - это карнавал", "Время лечит все раны",
        "Обезьяны тоже падают с деревьев", "Путь в тысячу миль начинается с одного шага",
        "Терпение – ключ к облегчению", "Доброе утро начинается с утра"
    )
    request_cases = (
        TranslatedRequest(user_id=user_id, original_text=original_text)
        for user_id, original_text in zip(
            (1, 1, 2, 3, 4, 5, 5, 5),
            request_texts
        )
    )

    for original_text, expected_text in zip(request_cases, response_texts):
        translated_response = await translated_async(data=original_text)
        assert translated_response == expected_text
