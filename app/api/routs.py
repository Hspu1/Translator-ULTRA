from typing import Annotated

from deep_translator import GoogleTranslator
from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import IntegrityError

from .routs_code import generate_user_id_code
from .schemas import TranslatedRequest
from app import TranslationModel
from app.infrastructure import async_session_maker
from app.utils import logger

generate_user_id_router = APIRouter()
translater_router = APIRouter()


@generate_user_id_router.post(path="/generate_user_id", status_code=201)
async def generate_user_id():
    response: dict[str, int] = await generate_user_id_code()
    return response


@translater_router.post(path="/translater", status_code=201)
async def translater(
        input_data: Annotated[TranslatedRequest, Depends()], request: Request
):
    redis = request.app.state.redis
    key = (
        f"translate:{input_data.user_id}:"
        f"{input_data.original_text}"
    )

    cached_data = await redis.get(key)
    if cached_data is not None:
        return {
            "translated_text": cached_data,
            "cached": True
        }

    translated = (
        GoogleTranslator(source='auto', target="ru").translate(
            input_data.original_text)
    )

    await redis.set(key, translated, ex=86400)

    translated_data = TranslationModel(
        user_id=input_data.user_id, original_word=input_data.original_text,
        translated_word=translated
    )
    if len(input_data.original_text) <= 25:
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    session.add(translated_data)

        except IntegrityError as e:
            logger.warning(f"IntegrityError при сохранении перевода: {e}")

    return {
        "translated_text": translated,
        "cached": False
    }
