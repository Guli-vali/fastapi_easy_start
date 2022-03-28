from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page, Params, paginate, LimitOffsetPage
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.events import EventInCreate, EventInResponse, ListOfEventsInResponse
from app.db.utils import get_db
from app.api.services.users import current_active_user
from app.api.services.events import events_dao_service
from app.api.services.users import current_active_user
from app.models.domain.users import UserDB


router = APIRouter()

@router.get(
    "",
    response_model=LimitOffsetPage[EventInResponse],
    name="events:list"
)
async def list_events(
    session: AsyncSession = Depends(get_db),
    user: UserDB = Depends(current_active_user),
):
        events = await events_dao_service.fetch_all(session)
        events_list = [EventInResponse.from_orm(event) for event in events]
        return paginate(events_list)

@router.get(
    "/{object_id}",
    response_model=EventInResponse,
    name="events:get-one"
)
async def get_event(
    session: AsyncSession = Depends(get_db),
    user: UserDB = Depends(current_active_user),
    object_id: int = Path(...),
):
        event = await events_dao_service.fetch_one(session, event_id=object_id)
        return EventInResponse.from_orm(event)

@router.post(
    "",
    response_model=EventInResponse,
    name="events:create")
async def create_event(
    event_create: EventInCreate,
    session: AsyncSession = Depends(get_db),
    user: UserDB = Depends(current_active_user),
) -> EventInResponse:
    created_id = await events_dao_service.insert_one(session, event_create)
    created_event = await events_dao_service.fetch_one(session, created_id)

    return EventInResponse.from_orm(created_event)

@router.put(
    "/{object_id}",
    response_model=EventInResponse,
    name="events:update")
async def update_event(
    event_update: EventInCreate,
    object_id: int = Path(...),
    session: AsyncSession = Depends(get_db),
    user: UserDB = Depends(current_active_user),
) -> EventInResponse:
    await events_dao_service.update_one(session, object_id, event_update)
    updated_event = await events_dao_service.fetch_one(session, object_id)
    
    return EventInResponse.from_orm(updated_event)


@router.delete(
    "/{object_id}",
    response_model=EventInResponse,
    name="events:delete")
async def delete_event(
    object_id: int = Path(...),
    session: AsyncSession = Depends(get_db),
    user: UserDB = Depends(current_active_user),
) -> EventInResponse:
    original_object = await events_dao_service.fetch_one(session, object_id)
    await events_dao_service.delete_one(session, object_id)

    return EventInResponse.from_orm(original_object)
