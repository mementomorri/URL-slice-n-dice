# URL-slice-n-dice

Высокопроизводительный сервис сокращения URL-адресов, построенный на Python, FastAPI и SQLite.

## 🚀 Возможности

- **Быстрое сокращение URL**: Создание коротких ссылок с уникальными 6-символьными кодами
- **Отслеживание кликов**: Статистика переходов с счетчиками в реальном времени
- **RESTful API**: Чистый дизайн API с автоматической документацией Swagger
- **Docker Ready**: Контейнеризованное развертывание с docker-compose
- **База данных SQLite**: Легковесное файловое хранилище данных
- **Валидация ввода**: Надежная проверка URL и обработка ошибок
- **CI/CD Pipeline**: Автоматическое тестирование и отчеты

## 📋 API Эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/api/v1/shorten` | Создать сокращенную ссылку |
| `GET` | `/s/{code}` | Перенаправление на оригинальный URL |
| `GET` | `/api/v1/stats/{code}` | Получить статистику URL |
| `GET` | `/health` | Проверка состояния |

## 🏃‍♂️ Быстрый старт

### Использование Docker (Рекомендуется)

```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd URL-slice-n-dice

# Собрать и запустить с Docker Compose
docker-compose up --build

# Открыть документацию API
open http://localhost:8000/docs
```

### Локальная разработка

```bash
# Активировать виртуальную среду
source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
uvicorn app.main:app --reload

# Открыть документацию API
open http://localhost:8000/docs
```

## 🧪 Тестирование

Запустите автоматизированный набор тестов:

```bash
# Запустить все тесты
pytest tests/ -v

# Запустить только быстрые тесты (исключить медленные тесты производительности)
pytest tests/ -m "not slow" -v

# Запустить тесты с покрытием
pytest tests/ --cov=app --cov-report=html

# Запустить конкретные категории тестов
pytest tests/ -m "integration" -v  # Только интеграционные тесты
pytest tests/ -m "unit" -v         # Только unit тесты
```

## 📖 Примеры использования API

### Создать сокращенную ссылку

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com"}'
```

**Ответ:**
```json
{
  "id": 1,
  "original_url": "https://example.com",
  "short_code": "abc123",
  "created_at": "2023-12-01T10:00:00Z",
  "clicks": 0
}
```

### Перейти по сокращенной ссылке

```bash
curl -L "http://localhost:8000/s/abc123"
```

### Получить статистику URL

```bash
curl "http://localhost:8000/api/v1/stats/abc123"
```

**Ответ:**
```json
{
  "original_url": "https://example.com",
  "short_code": "abc123", 
  "created_at": "2023-12-01T10:00:00Z",
  "clicks": 5
}
```

## 🏗️ Структура проекта

```
URL-slice-n-dice/
├── app/
│   ├── __init__.py          # Инициализация пакета
│   ├── main.py              # FastAPI приложение
│   ├── database.py          # Конфигурация базы данных
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── crud.py              # Операции с базой данных
│   └── utils.py             # Вспомогательные функции
├── .venv/                   # Виртуальная среда
├── requirements.txt         # Python зависимости
├── Dockerfile              # Конфигурация Docker образа
├── docker-compose.yml      # Конфигурация Docker Compose
├── tests/                  # Папка с тестами
│   ├── __init__.py         # Инициализация тестов
│   └── test_integration.py # Интеграционные тесты
└── README.md               # Этот файл
```

## 💾 База данных

Сервис использует SQLite для хранения данных со следующей схемой:

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(6) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0
);
```

Файл базы данных (`url_shortener.db`) автоматически создается при первом запуске.

## 🔧 Конфигурация

Приложение использует разумные значения по умолчанию, но может быть настроено через переменные окружения:

- `SQLALCHEMY_DATABASE_URL`: Строка подключения к базе данных (по умолчанию: SQLite)
- `HOST`: Хост сервера (по умолчанию: 0.0.0.0)  
- `PORT`: Порт сервера (по умолчанию: 8000)

## 🛡️ Обработка ошибок

API предоставляет комплексную обработку ошибок:

- **400 Bad Request**: Неверный формат URL
- **404 Not Found**: Короткий код не существует
- **422 Unprocessable Entity**: Ошибки валидации
- **500 Internal Server Error**: Ошибки сервера

## 📈 Производительность

- **Генерация коротких кодов**: Криптографически стойкие случайные коды
- **Индексация базы данных**: Оптимизированные запросы с правильными индексами
- **Stateless дизайн**: Горизонтально масштабируемая архитектура

## 🏆 Технические особенности

- **Соответствие PEP8**: Чистый, читаемый Python код
- **Type Hints**: Полное покрытие типизации
- **Async поддержка**: Асинхронные возможности FastAPI
- **Автодокументация**: Интерактивный Swagger UI
- **Готовность к контейнеризации**: Продакшен-готовый Docker setup