from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File

from configs import get_logger
from entities.models import Message
from entities.schemas import (
    DefaultResponsePayload,
    PagingResponsePayload,
    GetMessagesQuery,
)
from services import (
    get_all_messages,
    create_message,
)


router = APIRouter(prefix="/messages")
logger = get_logger(__name__)


@router.get("/health", response_model=DefaultResponsePayload, tags=["message"])
async def health():
    """
    Health check endpoint to monitor API availability.
    """
    return { "message": "healthy" }


@router.get("/all", response_model=DefaultResponsePayload, tags=["message"])
async def get_all(filter_query: Annotated[GetMessagesQuery, Query()]):
    """
    Get all messages.
    """
    exists = await get_all_messages(**filter_query.model_dump())
    data = map(lambda x: x.as_dict(), exists)
    return { "data": data, "message": "Get all messages successfully" }


@router.post("/audio", response_model=DefaultResponsePayload, tags=["message"])
async def upload(
    voice: Annotated[UploadFile, File(description="A voice audio file as UploadFile")],
):
    """
    Upload voice audio.
    Start a background service to handle uploading action.
    """
    # logger.info(f"===== blob =====: {voice}")
    # logger.info(f"===== blob file name =====: {blob.filename}")
    # logger.info(f"===== blob bytes data =====: {blob.file.read()}")
    voice_bytes = voice.file.read()
    message = Message(voice=voice_bytes)
    message = await create_message(message=message)
    return { "data": message.as_dict(), "message": "Upload voice audio successsfully" }
