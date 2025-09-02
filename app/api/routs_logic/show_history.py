from sqlalchemy import select, JSON

from app import TranslationModel
from app.infrastructure import async_session_maker


async def show_history_logic(user_id: int):
    async with async_session_maker() as session:
        stmt = select(TranslationModel).where(
            TranslationModel.user_id == user_id
        )

        result = await session.execute(stmt)
        history = result.scalars().all()

        return {
            "history": history
        }
