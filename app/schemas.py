from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class URLBase(BaseModel):
    """Базовая схема для URL"""

    original_url: str

    @validator("original_url")
    def validate_url(cls, v):
        """Валидация URL - должен начинаться с http:// или https://"""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return v


class URLCreate(URLBase):
    """Схема для создания URL"""

    pass


class URLResponse(URLBase):
    """Схема ответа при создании URL"""

    id: int
    short_code: str
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True


class URLStats(BaseModel):
    """Схема для статистики URL"""

    original_url: str
    short_code: str
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True
