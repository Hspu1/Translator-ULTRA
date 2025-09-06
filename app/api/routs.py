from typing import Annotated

from fastapi import (
    APIRouter, Depends, Query, BackgroundTasks
)

from .routs_logic import (
    generate_user_id_logic, translated, show_history_logic
)
from .schemas import TranslatedRequest, TranslationHistory
from .tasks import create_save_history_task


generate_user_id_router = APIRouter()
translator_router = APIRouter()
show_history_router = APIRouter()


@generate_user_id_router.post(path="/generate_user_id", status_code=201)
async def generate_user_id() -> dict[str, int]:
    response = await generate_user_id_logic()
    return response


@translator_router.post(path="/translator", status_code=201)
async def translator(
        input_data: Annotated[TranslatedRequest, Depends()],
        background_tasks: BackgroundTasks
) -> dict[str, str]:
    background_tasks.add_task(create_save_history_task, input_data)

    response = translated(data=input_data)
    return {
        "translated": response
    }


@show_history_router.get(path="/show_history", status_code=200)
async def show_history(user_id: Annotated[int, Query(ge=1)]) -> dict[str, list[TranslationHistory]]:
    response = await show_history_logic(user_id=user_id)
    return response
