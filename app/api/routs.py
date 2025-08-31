from typing import Annotated

from fastapi import APIRouter, Depends, Request

from .routs_logic import generate_user_id_logic, translator_logic
from .schemas import TranslatedRequest

generate_user_id_router = APIRouter()
translator_router = APIRouter()


@generate_user_id_router.post(path="/generate_user_id", status_code=201)
async def generate_user_id() -> dict[str, int]:
    response = await generate_user_id_logic()
    return response


@translator_router.post(path="/translator", status_code=201)
async def translator(
        input_data: Annotated[TranslatedRequest, Depends()], request: Request
) -> dict[str, str | bool]:
    response = await translator_logic(request=request, data=input_data)
    return response
