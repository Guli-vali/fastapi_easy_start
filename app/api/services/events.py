from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import NoResultFound

from app.db.models.event import Event
from app.models.schemas.events import EventInCreate, EventInResponse, ListOfEventsInResponse


class EventsDAO:

    async def fetch_all(self, session: AsyncSession) -> ScalarResult:
        stmt_select = select(Event)
        result = await session.execute(stmt_select)
        return result.scalars()

    async def fetch_one(self, session: AsyncSession, event_id: int) -> ScalarResult:
        try:
            stmt_select = select(Event).where(Event.id==event_id)
            result_select = await session.execute(stmt_select)
            return result_select.scalar_one()
        except:
            raise HTTPException(status_code=404, detail="Not found")


    async def insert_one(self, session: AsyncSession, event_create: EventInCreate) -> int:
        stmt_insert = (
            insert(Event).
            values(event_create.dict())
        )
        result_insert = await session.execute(stmt_insert)
        await session.commit()
        
        return result_insert.inserted_primary_key[0]

    async def delete_one(self, session: AsyncSession, object_id: int) -> None:
        stmt_delete = (
            delete(Event).
            where(Event.id == object_id)
        )
        await session.execute(stmt_delete)
        await session.commit()

    async def update_one(self, session: AsyncSession, object_id: int, event_update: EventInCreate) -> None:
        update_data = event_update.dict(exclude_unset=True)
        stmt_update = (
            update(Event).
            where(Event.id == object_id).
            values(update_data)
        )
        await session.execute(stmt_update)
        await session.commit()


events_dao_service = EventsDAO()
