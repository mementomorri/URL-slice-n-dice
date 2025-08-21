import secrets
import string
from typing import Optional

from sqlalchemy.orm import Session

from .models import URL


def generate_short_code(length: int = 6) -> str:
    """Генерирует случайный короткий код используя буквенно-цифровые символы."""
    alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_unique_short_code(db: Session, length: int = 6) -> str:
    """Генерирует уникальный короткий код, которого нет в базе данных."""
    while True:
        short_code = generate_short_code(length)
        # Проверяем, существует ли код уже в базе
        if not db.query(URL).filter(URL.short_code == short_code).first():
            return short_code
