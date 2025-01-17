import whisper
import torch

from tempfile import NamedTemporaryFile
from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from transformers import pipeline

from configs import get_logger
from entities.models import Message
from entities.schemas import (
    DefaultResponsePayload,
    PagingResponsePayload,
    GetMessagesQuery,
)
from services import (
    get_all_messages,
    get_message_by_ids,
    create_message,
    delete_message,
)


# torch.cuda.is_available()
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# model = whisper.load_model("base", device=DEVICE)


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
    data = []
    
    ## Not a good idea to store only voice in database. should transcribed text as well.
    for message in exists:
        with NamedTemporaryFile(suffix=".wav") as temp:
            with open(temp.name, "wb") as temp_file:
                temp_file.write(message.voice)
            
            ## Use normal whisper
            # result = model.transcribe(temp.name, fp16=False)
            # output = result.get("text", "")
            
            ## Use PhoWhisper
            transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small")
            result = transcriber(temp.name)
            output = result.get("text", "")
            data.append({ "id": message.id, "message": output })
    
    return { "data": data, "message": "Get all messages successfully" }


@router.post("/audio", response_model=DefaultResponsePayload, tags=["message"])
async def upload(
    file: Annotated[UploadFile, File(description="A voice audio file as UploadFile")],
):
    """
    Upload voice audio.
    Start a background service to handle uploading action.
    """
    # logger.info(f"===== file =====: {file}")
    # logger.info(f"===== file name =====: {file.filename}")
    # logger.info(f"===== file bytes data =====: {file.file.read()}")
    file_bytes = file.file.read()
    message = Message(voice=file_bytes)
    message = await create_message(message=message)
    
    with NamedTemporaryFile(suffix=".wav") as temp:
        with open(temp.name, "wb") as temp_file:
            temp_file.write(file_bytes)
        
        ## Use normal whisper
        # result = model.transcribe(temp.name, fp16=False)
        # output = result.get("text", "")
        
        ## Use PhoWhisper
        transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small")
        result = transcriber(temp.name)
        output = result.get("text", "")
    
    return { "data": output, "message": "Upload voice audio successsfully" }


@router.delete("/message/{message_id}", response_model=DefaultResponsePayload, tags=["message"])
async def delete_by_id(message_id: str):
    """
    Delete message by id.
    """
    exists = await get_message_by_ids(ids=[message_id])
    
    if len(exists) < 1:
        raise HTTPException(status_code=404, detail="Message not found")
    
    exist = exists[0]
    await delete_message(message=exist)
    
    return { "message": "Delete message successfully" }
