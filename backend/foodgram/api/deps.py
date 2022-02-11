from types import NoneType

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import credentials_exception
from core.security import get_current_user
from db.schema import users_table


async def get_token_from_headers(
    request: Request,
):
    token: str = request.headers.get('authorization')
    if isinstance(token, NoneType):
        raise credentials_exception
    elif not token.startswith('Token '):
        raise credentials_exception
    elif len(token.split(' ')) != 2:
        raise credentials_exception
    return token.split(' ')[1]


async def get_user_by_token(
        token: str,
        session: AsyncSession
):
    id = await get_current_user(token=token)
    query = select(users_table).where(
        id == users_table.c.id,
        token == users_table.c.token
    )
    curs = await session.execute(query)
    user_db = curs.fetchone()
    if isinstance(user_db, NoneType):
        raise credentials_exception
    user = dict(user_db)
    if user is None:
        raise credentials_exception
    return user
