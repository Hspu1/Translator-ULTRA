from sqlalchemy import select

from app import TranslationModel
from ..schemas import TranslationHistory
from app.core.infrastructure import async_session_maker


async def show_history_logic(user_id: int) -> dict[str, list[TranslationHistory]]:
    async with async_session_maker() as session:
        stmt = select(TranslationModel).where(
            TranslationModel.user_id == user_id
        )

        result = await session.execute(stmt)
        history = result.scalars().all()

        return {
            "history": history
        }
