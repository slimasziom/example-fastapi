from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base

# SQLALCHEMY_DB_URL = f"postgresql://postgres:postgres@localhost:5432/fastapi"
SQLALCHEMY_DB_URL = f'postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(SQLALCHEMY_DB_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
        

@pytest.fixture(scope="session")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Alembic:
    # command.upgrade("head")
    # command.downgrade("base")
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def client(session):
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
