from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_user_from_db
from core.exceptions import ValidationException
from core.security import get_password_hash, verify_password
from db.schema import users_table
from schema.user import (UserResponseSchema, UserCreateSchema,
                         ChangePasswordSchema)


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
    user_list = [UserResponseSchema(**dict(user)) for user in get_list_response]
    return user_list, count


async def change_password(
        user,
        body: ChangePasswordSchema,
        session: AsyncSession
):
    if not verify_password(body.current_password, user.password):
        raise ValidationException()
    hash_password = get_password_hash(body.new_password)
    query = update(users_table).where(
        user.id == users_table.c.id
    ).values(password=hash_password)
    await session.execute(query)
    await session.commit()


async def check_available(
        session: AsyncSession,
        username: str | None = None,
        email: str | None = None,
        field: str = "field"
):
    check_available_query = select([func.count()]).select_from(users_table)
    if username:
        check_available_query = check_available_query.where(
            username == users_table.c.username
        )
    elif email:
        check_available_query = check_available_query.where(
            email == users_table.c.email
        )
    else:
        raise ValidationException()
    available = await session.execute(check_available_query)
    if available.fetchone()[0] != 0:
        raise ValidationException(
            message={"detail": f"{field} is not available"}
        )


async def insert_user_to_db(
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        session: AsyncSession
):
    user_db = users_table.insert().values(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    curs = await session.execute(user_db)
    await session.commit()
    return curs.inserted_primary_key[0]


async def create_user(
        body: UserCreateSchema,
        session: AsyncSession,
):
    await check_available(
        username=body.username, session=session, field="username"
    )
    await check_available(
        email=body.email, session=session, field="email"
    )
    hash_password = get_password_hash(body.password)
    id = insert_user_to_db(
        username=body.username,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=hash_password
    )
    user = await get_user_from_db(
        session=session, id=id
    )
    return user
