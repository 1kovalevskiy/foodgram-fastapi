from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_user_from_db
from core.exceptions import credentials_exception
from core.security import verify_password, create_access_token
from db.schema import users_table
from schema.auth import LoginRequestSchema, LoginResponseSchema
from schema.user import UserSchema


async def create_token(
        session: AsyncSession,
        body: LoginRequestSchema,
):
    user = await get_user_from_db(email=body.email, session=session)
    if not verify_password(body.password, user.password):
        raise credentials_exception()
    access_token = create_access_token(data={"id": user.id})
    await write_new_token_to_db(session=session, token=access_token, user=user)
    return LoginResponseSchema(auth_token=access_token)


async def write_new_token_to_db(
        session: AsyncSession,
        token: str,
        user: UserSchema
):
    insert_token_query = update(users_table).where(
        user.id == users_table.c.id).values(token=token)
    await session.execute(insert_token_query)
    await session.commit()


async def delete_token(
        session: AsyncSession,
        token: str
):
    user = await get_user_from_db(session=session, token=token)
    delete_token_query = update(users_table).where(
        user.get('id') == users_table.c.id).values(token=None)
    await session.execute(delete_token_query)
    await session.commit()
