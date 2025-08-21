import pytest
import time
import tempfile
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

# Создаем временную базу данных для тестов
@pytest.fixture(scope="session")
def test_db():
    """Создает временную базу данных для тестов"""
    # Используем in-memory базу данных для тестов
    test_engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Создаем таблицы
    Base.metadata.create_all(bind=test_engine)
    print("✅ Test database tables created")
    
    yield test_engine, TestingSessionLocal, None
    
    # Очистка не нужна для in-memory базы данных

@pytest.fixture
def client(test_db):
    """Создает тестовый клиент с временной базой данных"""
    test_engine, TestingSessionLocal, db_path = test_db
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # Переопределяем зависимость базы данных
    app.dependency_overrides[get_db] = override_get_db
    print("✅ Database dependency overridden")
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Очищаем переопределение
    app.dependency_overrides.clear()

@pytest.fixture
def test_client(test_db):
    """Альтернативный тестовый клиент с явным переопределением"""
    test_engine, TestingSessionLocal, db_path = test_db
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # Переопределяем зависимость базы данных
    app.dependency_overrides[get_db] = override_get_db
    print("✅ Test client database dependency overridden")
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Очищаем переопределение
    app.dependency_overrides.clear()



# Клиент с очищенной базой данных для каждого теста
@pytest.fixture
def clean_client(test_db):
    """Тестовый клиент с очищенной базой данных для каждого теста"""
    test_engine, TestingSessionLocal, db_path = test_db
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # Переопределяем зависимость базы данных
    app.dependency_overrides[get_db] = override_get_db
    
    # Очищаем базу данных перед каждым тестом
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    print("✅ Test database cleaned and recreated")
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Очищаем переопределение
    app.dependency_overrides.clear()

class TestURLShortenerIntegration:
    """Интеграционные тесты для URL Shortener API"""
    
    def test_health_check_integration(self, clean_client):
        """Тестирует эндпоинт проверки состояния через TestClient"""
        response = clean_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "URL Shortener"
    
    def test_create_short_url_integration(self, test_client):
        """Тестирует создание короткой ссылки через TestClient"""
        url_data = {"original_url": "https://example.com"}
        response = test_client.post("/api/v1/shorten", json=url_data)
        print(f"Create URL response: {response.status_code}")
        print(f"Create URL data: {response.json()}")
        assert response.status_code == 200, f"URL creation failed: {response.text}"
        data = response.json()
        assert "short_code" in data
        assert len(data["short_code"]) == 6
        assert data["original_url"] == "https://example.com"
        assert data["clicks"] == 0
        return data["short_code"]
    
    def test_redirect_integration(self, test_client):
        """Тестирует перенаправление через TestClient"""
        # Сначала создаем короткую ссылку
        url_data = {"original_url": "https://httpbin.org/redirect/1"}
        response = test_client.post("/api/v1/shorten", json=url_data)
        print(f"URL creation response: {response.status_code}")
        print(f"URL creation data: {response.json()}")
        assert response.status_code == 200, f"URL creation failed: {response.text}"
        
        short_code = response.json()["short_code"]
        print(f"Created short_code: {short_code}")
        
        # Тестируем перенаправление
        response = test_client.get(f"/s/{short_code}")
        print(f"Redirect response: {response.status_code}")
        print(f"Redirect headers: {response.headers}")
        if response.status_code != 307:
            print(f"Redirect response text: {response.text}")
        assert response.status_code == 307
        assert "Location" in response.headers
    
    def test_stats_integration(self, test_client):
        """Тестирует получение статистики через TestClient"""
        # Создаем короткую ссылку
        url_data = {"original_url": "https://example.com"}
        response = test_client.post("/api/v1/shorten", json=url_data)
        short_code = response.json()["short_code"]
        
        # Получаем статистику
        response = test_client.get(f"/api/v1/stats/{short_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["short_code"] == short_code
        assert data["clicks"] == 0
    
    def test_invalid_url_validation_integration(self, test_client):
        """Тестирует валидацию неверного URL через TestClient"""
        url_data = {"original_url": "invalid-url"}
        response = test_client.post("/api/v1/shorten", json=url_data)
        assert response.status_code == 422
    
    def test_nonexistent_short_code_integration(self, test_client):
        """Тестирует обработку несуществующего кода через TestClient"""
        response = test_client.get("/s/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "Короткая ссылка не найдена" in data["detail"]
    
    def test_click_counter_integration(self, test_client):
        """Тестирует увеличение счетчика кликов"""
        # Создаем короткую ссылку
        url_data = {"original_url": "https://example.com"}
        response = test_client.post("/api/v1/shorten", json=url_data)
        short_code = response.json()["short_code"]
        
        # Получаем начальную статистику
        response = test_client.get(f"/api/v1/stats/{short_code}")
        initial_clicks = response.json()["clicks"]
        
        # Выполняем перенаправление
        test_client.get(f"/s/{short_code}")
        
        # Проверяем увеличение счетчика
        response = test_client.get(f"/api/v1/stats/{short_code}")
        final_clicks = response.json()["clicks"]
        assert final_clicks == initial_clicks + 1

@pytest.mark.integration
class TestDatabaseIntegration:
    """Тесты интеграции с базой данных"""
    
    def test_database_connection(self, test_db):
        """Тестирует подключение к базе данных"""
        test_engine, TestingSessionLocal, db_path = test_db
        db = TestingSessionLocal()
        assert db is not None
        db.close()
    
    def test_url_model_creation(self, test_db):
        """Тестирует создание модели URL"""
        from app.models import URL
        
        test_engine, TestingSessionLocal, db_path = test_db
        db = TestingSessionLocal()
        try:
            url = URL(
                original_url="https://test.com",
                short_code="TEST12"
            )
            db.add(url)
            db.commit()
            db.refresh(url)
            
            assert url.id is not None
            assert url.original_url == "https://test.com"
            assert url.short_code == "TEST12"
            assert url.clicks == 0
            
            # Очистка
            db.delete(url)
            db.commit()
        finally:
            db.close()

@pytest.mark.slow
class TestPerformanceIntegration:
    """Тесты производительности"""
    
    def test_multiple_url_creation(self, test_client):
        """Тестирует создание множественных URL"""
        urls = []
        for i in range(10):
            url_data = {"original_url": f"https://example{i}.com"}
            response = test_client.post("/api/v1/shorten", json=url_data)
            assert response.status_code == 200
            urls.append(response.json()["short_code"])
        
        assert len(set(urls)) == 10  # Все коды должны быть уникальными
    
    def test_concurrent_requests(self, test_client):
        """Тестирует обработку одновременных запросов"""
        import threading
        import time
        
        results = []
        errors = []
        
        def create_url():
            try:
                url_data = {"original_url": "https://example.com"}
                response = test_client.post("/api/v1/shorten", json=url_data)
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Создаем 5 одновременных запросов
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_url)
            threads.append(thread)
            thread.start()
        
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0
        assert all(status == 200 for status in results)
