from typing import Any, Coroutine
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user

from db import db_article
from db.schemas import ArticleResponseSchema, ArticleSchema, UserSchema
from db.database import get_db

router = APIRouter(
    prefix="/article",
    tags=['article']
)


@router.post('/', response_model=ArticleResponseSchema)
async def create_articlel(request: ArticleSchema, db: Session = Depends(get_db)) -> Coroutine[ArticleResponseSchema, Any, Any]:
    return await db_article.create_article(db, request)


@router.get('/{id}', response_model=ArticleResponseSchema)
async def get_article(
    id: int, 
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
) -> Coroutine[ArticleResponseSchema, Any, Any]:
    print(current_user)
    return await db_article.get_article(db, id)