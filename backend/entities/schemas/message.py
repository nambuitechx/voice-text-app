from pydantic import BaseModel, Field


class GetMessagesQuery(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)


class CreateMessagePayload(BaseModel):
    query: str
