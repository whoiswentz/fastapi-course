from typing import Any, Coroutine, Dict, Optional

from fastapi import APIRouter
from fastapi.param_functions import Depends
from pydantic import BaseModel
from auth.oauth2 import oauth2_scheme

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)


@router.get(
    path="/all",
    summary="Retreive all blog posts",
    description="This api calls simulates fetching all blogs",
    response_description="The list of avaiable blogs"
)
async def get_all(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Optional[Dict[str, str]]:
    if page and page_size:
        return {"page": page, "page_size": page_size}


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]


@router.post("/new")
async def create_blog(
    blog: BlogModel,
    token: str = Depends(oauth2_scheme)
) -> Coroutine[BlogModel, Any, Any]:
    return blog
