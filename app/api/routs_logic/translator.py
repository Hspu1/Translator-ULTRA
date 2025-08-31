from fastapi import Request
from sqlalchemy.exc import IntegrityError

from .translator_utils import translated, save_translated
from app.api.schemas import TranslatedRequest
from app.infrastructure import async_session_maker
from app.utils import logger


async def translator_logic(request: Request, data: TranslatedRequest):
    translated_obj, save_translated_obj = (
        translated(data=data), save_translated(data=data)
    )

    redis_cache = request.app.state.redis_cache
    key = (
        f"translate:{data.user_id}:"
        f"{data.original_text}"
    )

    cached_data = await redis_cache.get(key)
    if cached_data is not None:
        return {
            "translated_text": cached_data,
            "cached": True
        }

    await redis_cache.set(key, translated_obj, ex=86400)
    if len(data.original_text) <= 35:
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    session.add(save_translated_obj)

        except IntegrityError as e:
            logger.warning(f"IntegrityError при сохранении перевода: {e}")

    return {
        "translated_text": translated_obj,
        "cached": False
    }
