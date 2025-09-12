from sqlalchemy.exc import IntegrityError

from app.api.routs_logic.translator_utils import save_translated
from app.api.schemas import TranslatedRequest
from app.infrastructure import async_session_maker
from app.infrastructure.queue_config import broker
from app.utils import logger


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

    if len(data.original_text) <= 35:
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    session.add(save_translated_obj)

        except IntegrityError as e:
            logger.warning(f"IntegrityError при сохранении перевода: {e}")


async def create_save_history_task(data: TranslatedRequest):
    await save_history.kiq(data=data)
