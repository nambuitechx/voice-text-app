from sqlalchemy import select, delete

from entities.models import Message
from configs.database import AsyncSessionLocal
from configs.logger import get_logger


logger = get_logger(__name__)


async def get_all_messages(limit: int, offset: int) -> list[Message]:
    try:
        async with AsyncSessionLocal() as session:
            statement = select(Message).limit(limit=limit).offset(offset=offset).order_by(Message.updated_at.asc())
            result = await session.execute(statement=statement)
            messages = result.scalars().all()
            return messages
    except Exception as e:
        logger.error(f"Failed to get all messages: {str(e)}")
        raise e


async def get_message_by_ids(ids: list[str]) -> Message:
    try:
        async with AsyncSessionLocal() as session:
            statement = select(Message).where(Message.id.in_(ids)).order_by(Message.updated_at.desc())
            result = await session.execute(statement=statement)
            messages = result.scalars().all()
            return messages
    except Exception as e:
        logger.error(f"Failed to get messages by ids: {str(e)}")
        raise e


async def create_message(message: Message) -> Message:
    try:
        async with AsyncSessionLocal() as session:
            session.add(message)
            await session.commit()
            return message
    except Exception as e:
        logger.error(f"Failed to create message: {str(e)}")
        raise e


async def delete_message(message: Message):
    try:
        async with AsyncSessionLocal() as session:
            statement = delete(Message).where(Message.id == message.id)
            await session.execute(statement)
            await session.commit()
    except Exception as e:
        logger.error(f"Failed to delete message: {str(e)}")
        raise e
