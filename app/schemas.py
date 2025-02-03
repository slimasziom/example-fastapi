from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    
class UserOut(BaseModel):
    uuid: int
    email: EmailStr
    created_at: datetime


    class Config:
        from_attributes = True


        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    uuid: int
    created_at: datetime
    owner_uuid: int
    owner: UserOut
    
    class Config:
        from_attributes = True
        

class PostOut(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: Optional[str] = None


class Vote(BaseModel):
    post_uuid: int
    dir: conint(ge=0, le=1)
