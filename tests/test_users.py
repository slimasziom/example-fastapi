from fastapi import status
import pytest
from jose import jwt
from app import schemas
from .database import client, session
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == "Hello from ubuntu"
#     assert res.status_code == status.HTTP_200_OK
    

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "pass123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]) 

    uuid = payload.get("user_id")
    assert uuid == test_user["uuid"]
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email@gmailcom", "password1234", status.HTTP_403_FORBIDDEN),
    ("hello1234@gmail.com", "wrong_password", status.HTTP_403_FORBIDDEN),
    ("hello1234@gmail.com", "password1234", status.HTTP_403_FORBIDDEN),
    (None, "password1234", status.HTTP_403_FORBIDDEN),
    ("hello1234@gmail.com", None, status.HTTP_403_FORBIDDEN),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'