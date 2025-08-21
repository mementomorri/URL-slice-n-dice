from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class URL(Base):
    """Модель для хранения URL-адресов"""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(6), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)
