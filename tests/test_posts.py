from fastapi import status
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    
    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].uuid}")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    random_uuid = 888888
    res = authorized_client.get(f"/posts/{random_uuid}")

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].uuid}")

    post = schemas.PostOut(**res.json())
    assert post.Post.uuid == test_posts[0].uuid
    assert post.Post.content == test_posts[0].content
    
    assert res.status_code == status.HTTP_200_OK
    

@pytest.mark.parametrize("title, content, published", [
    ("Awesome new title", "awesome new content", True),
    ("Favourite pizza", "I love pepperoni!", False),
    ("Talles scyscrapers", "OMG", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_uuid == test_user["uuid"]
    
    
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_uuid == test_user["uuid"]
    

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "title", "content": "content"})
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].uuid}")
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].uuid}")
    
    assert res.status_code == status.HTTP_204_NO_CONTENT
    
    
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    random_uuid = 888888
    res = authorized_client.delete(f"/posts/{random_uuid}")
    
    assert res.status_code == status.HTTP_404_NOT_FOUND
    
    
def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.delete(f"/posts/{3}")
    
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "uuid": test_posts[0].uuid
    }
    
    res = authorized_client.put(f"/posts/{test_posts[0].uuid}", json=data)
    updated_post = schemas.Post(**res.json())
    
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
  
  
def test_update_post_other_user(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "uuid": test_posts[0].uuid
    }
    
    res = authorized_client.put(f"/posts/{test_posts[3].uuid}", json=data)
    
    assert res.status_code == status.HTTP_403_FORBIDDEN
    
    
def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].uuid}")
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    random_uuid = 888888
    data = {
        "title": "updated title",
        "content": "updated content",
        "uuid": random_uuid
    }
    res = authorized_client.put(f"/posts/{random_uuid}", json=data)
    
    assert res.status_code == status.HTTP_404_NOT_FOUND
