import os
import socket

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    try:
        async with SessionLocal() as session:
            try:
                yield session
            except (SQLAlchemyError, OSError):
                await session.rollback()
                raise HTTPException(
                    status_code=503,
                    detail="Service temporarily unavailable"
                )
    except (SQLAlchemyError, OSError):
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable"
        )