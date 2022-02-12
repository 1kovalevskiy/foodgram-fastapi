from types import NoneType

from pydantic import BaseModel, constr, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import credentials_exception, not_found_exception
from core.security import get_current_user
from db.schema import users_table
from schema.user import UserSchema


class UserData(BaseModel):
    id: int | None
    username: constr(max_length=255) | None
    email: EmailStr | None
    token: str | None


async def get_user_from_db(
        session: AsyncSession,
        **data
):
    query = select(users_table)
    user_data = UserData(**data)
    if user_data.id:
        query = query.where(user_data.id == users_table.c.id)
    if user_data.username:
        query = query.where(user_data.username == users_table.c.username)
    if user_data.email:
        query = query.where(user_data.email == users_table.c.email)
    if user_data.token:
        id = await get_current_user(token=user_data.token)
        query = query.where(user_data.token == users_table.c.token).where(
            id == users_table.c.id
        )
    user_db = await session.execute(query)
    user = user_db.fetchone()
    if user is None:
        raise not_found_exception()
    return UserSchema(**dict(user))