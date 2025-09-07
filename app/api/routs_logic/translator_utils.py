from asyncio import get_event_loop

from deep_translator import GoogleTranslator

from app.api.schemas import TranslatedRequest
from app import TranslationModel


async def translated_async(data: TranslatedRequest) -> str:
    loop = get_event_loop()

    return await loop.run_in_executor(
        None,
        lambda: GoogleTranslator(
            source='auto', target="ru").translate(data.original_text)
    )


async def save_translated(data: TranslatedRequest) -> TranslationModel:
    translated_data = await translated_async(data=data)

    save_translated_data = TranslationModel(
        user_id=data.user_id, original_word=data.original_text,
        translated_word=translated_data
    )

    return save_translated_data
