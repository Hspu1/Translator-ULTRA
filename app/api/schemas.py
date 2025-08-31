from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator


def strip_whitespace(v):
    return v.strip()


class TranslatedRequest(BaseModel):
    user_id: int
    original_text: Annotated[
        str, Field(min_length=1, max_length=500),
        BeforeValidator(strip_whitespace)
    ]
