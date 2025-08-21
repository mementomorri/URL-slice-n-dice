from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

# Создание таблиц базы данных
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"❌ Failed to create database tables: {e}")

app = FastAPI(
    title="URL Shortener",
    description="Сервис сокращения URL-адресов, аналогичный bit.ly",
    version="1.0.0",
)


@app.post("/api/v1/shorten", response_model=schemas.URLResponse)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    """Создает сокращенную ссылку."""
    try:
        db_url = crud.create_url(db=db, url=url)
        return db_url
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Ошибка создания короткой ссылки: {str(e)}"
        )


@app.get("/s/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """Перенаправляет на оригинальный URL и увеличивает счетчик кликов."""
    db_url = crud.get_url_by_code(db=db, short_code=short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")

    # Увеличиваем счетчик кликов
    crud.increment_clicks(db=db, url=db_url)

    # Перенаправляем на оригинальный URL
    return RedirectResponse(url=db_url.original_url, status_code=307)


@app.get("/api/v1/stats/{short_code}", response_model=schemas.URLStats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    """Получает статистику для сокращенной ссылки."""
    db_url = crud.get_url_by_code(db=db, short_code=short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")

    return db_url


@app.get("/health")
def health_check():
    """Эндпоинт проверки состояния."""
    return {"status": "healthy", "service": "URL Shortener"}
