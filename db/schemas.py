from typing import List
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserA(BaseModel):
    username: str

    class Config:
        orm_mode: bool = True


class ArticleResponseSchema(BaseModel):
    title: str
    content: str
    published: bool
    user: UserA

    class Config:
        orm_mode: bool = True


class UserResponseSchema(BaseModel):
    username: str
    email: str
    articles: List["ArticleResponseSchema"] = []

    class Config:
        orm_mode: bool = True


class ArticleSchema(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
