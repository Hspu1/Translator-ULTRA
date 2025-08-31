from deep_translator import GoogleTranslator

from app.api.schemas import TranslatedRequest
from app import TranslationModel


def translated(data: TranslatedRequest):
    translated_data = (
        GoogleTranslator(source='auto', target="ru"
        ).translate(data.original_text)
    )

    return translated_data


def save_translated(data: TranslatedRequest):
    translated_data = translated(data=data)

    save_translated_data = TranslationModel(
        user_id=data.user_id, original_word=data.original_text,
        translated_word=translated_data
    )

    return save_translated_data
