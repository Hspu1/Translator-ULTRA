from sqlalchemy import (
    Column, Integer, DateTime, func, ForeignKey,
    String, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship

from .config import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    bp_translations = relationship(
        "TranslationModel",  # связь с другой таблицей
        back_populates="bp_user",  # двусторонняя связь
        cascade="all, delete-orphan"  # автоматическое управление
        # del user => del user data (для целостности данных)
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TranslationModel(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )  # ondelete="CASCADE" - удаление не только тех данных, которые мы указали,
    # но и всех остальных, которые имеют связь с указанными
    original_word = Column(String(50), nullable=False, index=True)
    translated_word = Column(String(50), nullable=False, index=True)
    bp_user = relationship("UserModel", back_populates="bp_translations")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # исключение дубликатов
    __table_args__ = (
        UniqueConstraint(
            'user_id', 'original_word',
            name='uq_user_original_word'
        ),
        # составные индексы для запросов, где задействованы сразу 2 колонки
        Index('idx_user_created_at', 'user_id', 'created_at'),
        Index('idx_original_translated', 'original_word', 'translated_word'),
        Index('idx_user_original', 'user_id', 'original_word'),
    )
