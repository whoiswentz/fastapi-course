from typing import List
from fastapi import FastAPI, Request, WebSocket
from starlette.websockets import WebSocketDisconnect
from router import blog_route, user_routes, article_route, file_route
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

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


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connhect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self.active_connections.remove(ws)

    async def send_message(self, message: str, ws: WebSocket) -> None:
        await ws.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


connection_manager = ConnectionManager()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(ws: WebSocket, client_id: int) -> None:
    await connection_manager.connhect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await connection_manager.send_message(f'{data}', ws)
            await connection_manager.broadcast(f'{client_id} - {data}')
    except WebSocketDisconnect:
        connection_manager.disconnect(ws)
        await connection_manager.broadcast(f'{client_id} left')

app.include_router(blog_route.router)
app.include_router(file_route.router)
app.include_router(article_route.router)
app.include_router(user_routes.router)
app.include_router(authentication.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
