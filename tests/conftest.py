import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

# SQLALCHEMY_DB_URL = f"postgresql://postgres:postgres@localhost:5432/fastapi"
SQLALCHEMY_DB_URL = f'postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(SQLALCHEMY_DB_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
        

@pytest.fixture()
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

@pytest.fixture()
def client(session):
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello1234@gmail.com",
                 "password": "pass1234"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == status.HTTP_201_CREATED
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    
    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {"email": "hello12345@gmail.com",
                 "password": "pass12345"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == status.HTTP_201_CREATED
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["uuid"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_uuid": test_user['uuid']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_uuid": test_user['uuid']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_uuid": test_user['uuid']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_uuid": test_user2['uuid']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
        
    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    
    # session.add_all([models.Post("title": "asdf", content="asdf", owner_uuid=test_user['uuid']),
    #                  models.Post("title": "asdf", content="asdf", owner_uuid=test_user['uuid')])
                  
    session.add_all(posts)  
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts
