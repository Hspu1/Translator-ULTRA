from asyncio import to_thread

from deep_translator import GoogleTranslator

from app.api.schemas import TranslatedRequest
from app import TranslationModel


async def translated_async(data: TranslatedRequest) -> str:
    translator = GoogleTranslator(source='auto', target="ru")
    translated_text = await to_thread(translator.translate, data.original_text)

    return translated_text


async def save_translated(data: TranslatedRequest) -> TranslationModel:
    translated_data = await translated_async(data=data)

    save_translated_data = TranslationModel(
        user_id=data.user_id, original_word=data.original_text,
        translated_word=translated_data
    )

    return save_translated_data
