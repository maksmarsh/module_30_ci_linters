import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db

# URL-адрес базы данных SQLite для тестирования
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Создание движка SQLAlchemy
engine = create_engine(
 URL_DATABASE_SQLITE,
 connect_args={"check_same_thread": False},
 poolclass=StaticPool,
)

# Создайте объект sessionmaker для управления сеансами
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
db_session def():
    """Создайте новый сеанс работы с базой данных с откатом в конце теста."""
 connection = engine.connect()
 transaction = connection.begin()
 session = TestingSessionLocal(bind=connection)
    yield session
 session.close()
 transaction.rollback()
 connection.close()


@pytest.fixture(scope="function")
test_client def(db_session):
    """Создайте тестового клиента, который использует фикстур override_get_db для возврата сеанса."""

    override_get_db def():
        try:
            yield db_session
        finally:
 db_session.close()

 app.dependency_overrides[get_db] = override_get_db
    с помощью TestClient(app) в качестве test_client:
        yield test_client
