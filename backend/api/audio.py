from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File

from entities.schemas import (
    DefaultResponsePayload,
    PagingResponsePayload,
)
from configs import get_logger


router = APIRouter(prefix="/audio")
logger = get_logger(__name__)


@router.get("/health", response_model=DefaultResponsePayload, tags=["audio"])
async def health():
    """
    Health check endpoint to monitor API availability.
    """
    return { "message": "healthy" }


@router.post("/speak", response_model=DefaultResponsePayload, tags=["audio"])
async def upload(
    blob: Annotated[UploadFile, File(description="One audio file blob as UploadFile")],
):
    """
    Upload voice audio.
    Start a background service to handle uploading action.
    """
    # logger.info(f"===== blob =====: {blob}")
    # logger.info(f"===== blob file name =====: {blob.filename}")
    # logger.info(f"===== blob bytes data =====: {blob.file.read()}")
    blob_bytes = blob.file.read()
    logger.info(blob_bytes)
    return { "message": "Upload voice audio successsfully" }
