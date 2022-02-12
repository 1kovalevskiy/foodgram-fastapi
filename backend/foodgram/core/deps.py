from types import NoneType

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_user_from_db
from core.exceptions import credentials_exception
from schema.user import UserSchema


async def get_user_from_auth_header(
        request: Request,
        session: AsyncSession
):
    token = await get_token_from_headers(
        request=request
    )
    user = await get_user_from_db(
        token=token, session=session
    )
    return user


async def get_token_from_headers(
    request: Request,
):
    token: str = request.headers.get('authorization')
    if isinstance(token, NoneType):
        raise credentials_exception()
    elif not token.startswith('Token '):
        raise credentials_exception()
    elif len(token.split(' ')) != 2:
        raise credentials_exception()
    return token.split(' ')[1]


def get_field_for_pagination(
        page: int,
        limit: int,
        count: int,
        base_url: str
):
    fields = {
        "count": count,
        "next": None,
        "previous": None
    }
    if page > 1:
        fields["previous"] = base_url + f'?page={page - 1}&limit={limit}'
    if page * limit < count:
        fields["next"] = base_url + f'?page={page + 1}&limit={limit}'
    return fields
