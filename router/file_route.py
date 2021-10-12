from typing import Any, Coroutine
from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File

import shutil

from starlette.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['files']
)


@router.post('/upload')
async def post_file(file: bytes = File(...)) -> Coroutine[Any, Any, Any]:
    content = file.decode('utf-8')
    lines = content.split('\n')

    return {'lines': lines}


@router.post('/upload2')
async def post_file(file: UploadFile = File(...)) -> Coroutine[Any, Any, Any]:
    path = f'files/{file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        'filename': path,
        'type': file.content_type
    }


@router.get('/donwload/{filename}', response_class=FileResponse)
async def download(filename: str) -> Coroutine[FileResponse, Any, Any]:
    return f'files/{filename}'
