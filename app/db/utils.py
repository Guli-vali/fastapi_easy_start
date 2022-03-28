from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)

async def get_db():
    async with async_session() as session:
        yield session

# sync_engine = create_engine(settings.database_url, echo=True)
# sync_session = sessionmaker(bind=sync_engine)
# def get_db_sync():
#     session = sync_session()
#     try:
#         yield session
#     except Exception:
#         session.rollback()
#         raise
#     finally:
#         session.close()
