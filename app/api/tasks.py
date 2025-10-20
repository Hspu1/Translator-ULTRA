from sqlalchemy.exc import IntegrityError

from app import TranslationModel
from app.api.routs_logic.translator_utils import save_translated
from app.api.schemas import TranslatedRequest
from app.infrastructure import async_session_maker
from app.infrastructure.queue_config import broker
from app.utils import logger


async def save_history_util(session, data: TranslatedRequest, obj: TranslationModel) -> bool:
    if len(data.original_text) <= 35:
        try:
            async with session.begin():
                session.add(obj)
                return True

        except IntegrityError as e:
            logger.warning(f"IntegrityError при сохранении перевода: {e}")
            return False

    return False


@broker.task(
    task_name="save_translation_history",

    timeout=10,
    retry_count=3, retry_backoff=True,
    retry_backoff_delay=1, retry_jitter=True,
    # 1) 0.7 - 1.3 секунды 2) 1.4 - 2.6 секунды 3) 2.8 - 5.2 секунды
    priority=0
)
async def save_history(data: TranslatedRequest):
    save_translated_obj = await save_translated(data=data)
    async with async_session_maker() as session:
        await save_history_util(
            session=session, data=data, obj=save_translated_obj
        )


async def create_save_history_task(data: TranslatedRequest):
    await save_history.kiq(data=data)
