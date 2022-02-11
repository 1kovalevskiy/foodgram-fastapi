from fastapi import Depends, Body, HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from paginate_sqlalchemy import SqlalchemyOrmPage

from api.auth.validators import ChangePassword
from api.users.validators import UserCreate
from core.security import get_password_hash, verify_password
from db.base import get_session
from db.schema import users_table


async def get_user_list(
        session: AsyncSession,
        page: int = 1,
        limit: int = 10,
):
    get_length_query = select([func.count()]).select_from(users_table)
    get_length_response = await session.execute(get_length_query)
    count = get_length_response.fetchone()[0]
    if (page-1)*limit >= count:
        return [], count
    get_list_query = select(users_table).limit(limit).offset((page-1)*limit)
    get_list_response = await session.execute(get_list_query)
    user_list = [dict(user) for user in get_list_response]
    return user_list, count


async def get_user(
        session: AsyncSession,
        id: int
):
    get_user_query = select(users_table).where(id == users_table.c.id)
    get_user_data = await session.execute(get_user_query)
    try:
        user = dict(get_user_data.fetchone())
    except TypeError:
        raise HTTPException(
            status_code=404, detail="user not found"
        )
    return user


async def create_user(
        body: UserCreate,
        session: AsyncSession,
):
    check_username_available_query = select([func.count()]).select_from(
        users_table).where(body.username == users_table.c.username)
    username_available = await session.execute(check_username_available_query)
    if username_available.fetchone()[0] != 0:
        raise HTTPException(
            status_code=401, detail="username is not available"
        )
    check_email_available_query = select([func.count()]).select_from(
        users_table).where(body.email == users_table.c.email)
    email_available = await session.execute(check_email_available_query)
    if email_available.fetchone()[0] != 0:
        raise HTTPException(
            status_code=401, detail="email is not available"
        )
    unhash_password = body.password
    hash_password = get_password_hash(unhash_password)
    user_db = users_table.insert().values(
        username=body.username,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=hash_password,
    )
    curs = await session.execute(user_db)
    await session.commit()
    return await get_user(
        session=session, id=curs.inserted_primary_key[0]
    )


async def change_password(
        user,
        body: ChangePassword,
        session: AsyncSession
):
    unhash_password = body.current_password
    if not verify_password(unhash_password, user.get('password')):
        raise HTTPException(
            status_code=400, detail="password is not correct"
        )
    hash_password = get_password_hash(body.new_password)
    query = update(users_table).where(
        int(user.get('id')) == users_table.c.id
    ).values(password=hash_password)
    await session.execute(query)
    await session.commit()
