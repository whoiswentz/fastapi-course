from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from .database import Base
from sqlalchemy import Column
from typing import List

class UserModel(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String)
    email: str = Column(String)
    password: str = Column(String)

    items = relationship("ArticleModel", back_populates='user')


class ArticleModel(Base):
    __tablename__ = "articles"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    content: str = Column(String)
    published: bool = Column(Boolean)
    user_id: int = Column(Integer, ForeignKey('users.id'))

    user: UserModel = relationship("UserModel", back_populates='items')