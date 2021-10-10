from typing import Optional, Dict
from fastapi import FastAPI
from router import blog_route, user_routes, article_route
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(blog_route.router)
app.include_router(article_route.router)
app.include_router(user_routes.router)
app.include_router(authentication.router)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello, World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, query: Optional[str] = None) -> Dict[str, str]:
    return {'item_id': item_id, "query": query}
