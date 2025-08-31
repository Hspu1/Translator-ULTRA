from sqlalchemy import insert

from app import UserModel
from app.infrastructure import async_session_maker


async def generate_user_id_code() -> dict[str, int]:
    async with async_session_maker() as session:
        async with session.begin():
            stmt = insert(UserModel).returning(UserModel.id)

            result = await session.execute(stmt)
            user_id = result.scalar_one()

        return {
            "user_id": user_id
        }
