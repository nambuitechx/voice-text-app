# -*- coding: utf-8 -*-
from asyncio import current_task

from configs.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool


def get_database_engine():
    url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    engine = create_async_engine(
        url,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=20,
        max_overflow=30,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
        echo=True,
    )
    
    return engine


async_session_maker = sessionmaker(bind=get_database_engine(), class_=AsyncSession, expire_on_commit=False)

AsyncSessionLocal = async_scoped_session(async_session_maker, scopefunc=current_task)
