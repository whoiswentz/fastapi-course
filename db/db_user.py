from typing import List, Optional
from db.hash import Hash
from sqlalchemy.orm.session import Session
from .schemas import UserSchema
from db.models import UserModel


def create_user(db: Session, request: UserSchema) -> UserModel:
    new_user = UserModel(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).all()


def get_user_by_id(db: Session, id: int) -> UserModel:
    return (db.query(UserModel).filter(UserModel.id == id).first())


def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    return (db.query(UserModel).filter(UserModel.username == username).first())


def update_user(db: Session, id: int, request: UserSchema) -> UserModel:
    user = db.query(UserModel).filter(UserModel.id == id)
    user.update({
        UserModel.username: request.username,
        UserModel.email: request.email,
        UserModel.password: Hash.bcrypt(request.password)
    })
    db.commit()

    return get_user_by_id(db, id)


def delete_user(db: Session, id: int) -> str:
    user = db.query(UserModel).filter(UserModel.id == id).first()
    db.delete(user)
    db.commit()

    return 'ok'
