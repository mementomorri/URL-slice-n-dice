import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///url_shortener.db"

# Создание движка SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Необходимо для SQLite
)

# Создание класса SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса
Base = declarative_base()


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
