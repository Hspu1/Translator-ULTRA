from fastapi import Request

from .translator_utils import translated, save_translated
from app.api.schemas import TranslatedRequest


async def translator_logic(data: TranslatedRequest, request: Request):
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

    return {
        "translated_text": translated_obj,
        "cached": False
    }
