from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File

from entities.schemas import (
    DefaultResponsePayload,
    PagingResponsePayload,
)
from configs import get_logger


router = APIRouter(prefix="/audio")
logger = get_logger(__name__)


@router.get("/health-check")
async def health_check():
    """
    Health check endpoint to monitor API availability.
    """
    return {"status": "success"}


@router.post("/speak", response_model=DefaultResponsePayload, tags=["audio"])
async def upload(
    blob: Annotated[UploadFile, File(description="One audio file blob as UploadFile")],
):
    """
    Upload voice audio.
    Start a background service to handle uploading action.
    """
    logger.info(blob)
    
    return { "message": "Upload voice audio successsfully" }
