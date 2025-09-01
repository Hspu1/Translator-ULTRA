from abc import ABC, abstractmethod
from typing import Any


class AbstractCache(ABC):
    # объединяет абстракцию для работы с кэшэм
    # и класс для его мока в тестах
    @abstractmethod
    async def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int) -> None:
        pass

    @abstractmethod
    async def aclose(self) -> None:
        pass
