from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.schemas import UserResponseSchema, UserSchema
from db.database import get_db
from db.models import UserModel
from db import db_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserResponseSchema)
async def create_user(request: UserSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    return db_user.create_user(db, request)


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(db: Session = Depends(get_db)) -> List[UserResponseSchema]:
    return db_user.get_all_users(db)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user_by_id(id: int, db: Session = Depends(get_db)) -> UserResponseSchema:
    return db_user.get_user_by_id(db, id)


@router.put("/{id}", response_model=UserResponseSchema)
async def update_user(id: int, request: UserSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    return db_user.update_user(db, id, request)


@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)) -> str:
    return db_user.delete_user(db, id)