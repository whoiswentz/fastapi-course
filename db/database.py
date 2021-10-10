from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DAGTABASE_URL = "sqlite:///.fastapi-pratice.db"

engine = create_engine(SQLALCHEMY_DAGTABASE_URL, connect_args={
    "check_same_thread": False
})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[sessionmaker, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
