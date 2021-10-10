from typing import Optional, Dict
from fastapi import FastAPI
from router import blog_route, user_routes, article_route
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

models.Base.metadata.create_all(engine)

app = FastAPI(
    name="FastAPI Course"
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
