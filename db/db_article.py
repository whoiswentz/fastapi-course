from typing import Any, Coroutine
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from db.models import ArticleModel
from db.schemas import ArticleSchema


async def create_article(db: Session, request: ArticleSchema) -> Coroutine[ArticleModel, Any, Any]:
    new_article = ArticleModel(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


async def get_article(db: Session, id: int) -> Coroutine[ArticleModel, Any, Any]:
    article = db.query(ArticleModel).filter(ArticleModel.id == id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Article with id {id} not found'
        )
    return article
