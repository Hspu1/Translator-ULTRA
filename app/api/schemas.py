from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator


def strip_whitespace(v):
    return v.strip()


class TranslatedRequest(BaseModel):
    user_id: int
    original_text: Annotated[
        str, Field(min_length=1, max_length=5000),
        BeforeValidator(strip_whitespace)
    ]


class TranslationHistory(BaseModel):
    user_id: int
    id: int
    translated_word: str
    original_word: str
    created_at: datetime
