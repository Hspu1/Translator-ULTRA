from fastapi import APIRouter

from .routs_code import generate_user_id_code


generate_user_id_router = APIRouter()


@generate_user_id_router.post(path="/generate_user_id", status_code=201)
async def generate_user_id():
    response: dict[str, int] = await generate_user_id_code()
    return response
