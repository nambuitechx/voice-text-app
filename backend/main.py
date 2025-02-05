from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# from api import ALL_ROUTERS
from services import (
    SystemException,
    default_exception_handler,
    system_exception_handler,
    http_exception_handler,
    validation_exception_handler,   
)
from configs.websocket import WebSocketConnectionManager
from configs.logger import get_logger

app = FastAPI()
logger = get_logger(__name__)
ws_connection_manager = WebSocketConnectionManager()


# Exception Handler
app.add_exception_handler(Exception, default_exception_handler)
app.add_exception_handler(SystemException, system_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, or you can specify specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# # Include router
# for router in ALL_ROUTERS:
#     app.include_router(prefix="/api/v1", router=router)


@app.get("/health")
async def health_check():
    return {"message": "Hello World"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info(f"Client '{client_id}' is trying to connect to websocket...")
    await ws_connection_manager.connect(websocket=websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_connection_manager.send_personal_message(f"You wrote: {data}", websocket)
            await ws_connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        ws_connection_manager.disconnect(websocket)
        logger.info(f"Client '{client_id}' disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)