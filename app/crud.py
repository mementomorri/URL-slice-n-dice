from sqlalchemy.orm import Session

from . import models, schemas
from .utils import get_unique_short_code


def create_url(db: Session, url: schemas.URLCreate) -> models.URL:
    """Создает новый URL с уникальным коротким кодом."""
    short_code = get_unique_short_code(db)
    db_url = models.URL(original_url=url.original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_code(db: Session, short_code: str) -> models.URL:
    """Получает URL по короткому коду."""
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()


def increment_clicks(db: Session, url: models.URL) -> None:
    """Увеличивает счетчик кликов для URL."""
    url.clicks += 1
    db.commit()
