# CI/CD Pipeline Documentation

## Обзор

Этот репозиторий использует GitHub Actions для автоматизации процессов разработки, тестирования и развертывания.

## Workflows

### 1. CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

Основной pipeline, который запускается при push в `main`/`develop` и pull requests.

**Jobs:**
- **test**: Тестирование и отчеты

### 2. Quick Code Check (`.github/workflows/quick-check.yml`)

Быстрая проверка кода для pull requests.

**Jobs:**
- **quick-check**: Линтер, форматирование, быстрые тесты

## Настройка Secrets

Для работы pipeline дополнительные secrets не требуются. Pipeline работает только с тестированием и отчетами.

## Локальное тестирование

### Установка зависимостей для разработки

```bash
pip install -r requirements.txt
```

### Запуск линтера

```bash
# flake8
flake8 app/

# black
black app/

# isort
isort app/
```

### Запуск тестов

```bash
# Все тесты
pytest

# Только быстрые тесты
pytest -m "not slow"

# С покрытием
pytest --cov=app --cov-report=html

# Интеграционные тесты
pytest tests/ -v
```

### Проверка безопасности

```bash
# Зависимости
safety check

# Код
bandit -r app/
```

## Артефакты

Pipeline создает следующие артефакты:

1. **test-reports**: Отчеты о тестировании
   - HTML отчет о покрытии кода
   - XML отчет для Codecov
   - Markdown отчет о тестах

## Конфигурационные файлы

- `pytest.ini`: Конфигурация pytest
- `.flake8`: Конфигурация flake8
- `pyproject.toml`: Конфигурация инструментов разработки

## Требования к покрытию кода

Минимальное покрытие кода: **80%**

## Уведомления

Pipeline отправляет уведомления о:
- Успешном/неуспешном выполнении
- Результатах тестирования
- Покрытии кода

## Troubleshooting

### Частые проблемы

1. **Ошибки линтера**: Запустите `black app/` и `isort app/`
2. **Низкое покрытие**: Добавьте тесты для непокрытых функций
3. **Ошибки тестирования**: Проверьте тесты и зависимости

### Логи

Логи выполнения доступны в GitHub Actions UI:
`https://github.com/{owner}/{repo}/actions`
