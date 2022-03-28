from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from app.db.utils import Base
from app.db.utils import get_db
from app.db.utils import async_session
from app.models.domain.users import UserDB


class UserTable(Base, SQLAlchemyBaseUserTable):
    __tablename__ = 'Users'


async def get_user_db(session: async_session = Depends(get_db)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)
