from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.validators import LoginData
from api.deps import get_user_by_token
from core.security import verify_password, create_access_token, get_current_user
from core.settings import SECRET_KEY
from db.schema import users_table


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()


async def check_user_data(
        session: AsyncSession,
        body: LoginData,
):
    get_user_query = select(users_table).where(
        body.email == users_table.c.email)
    user_db = await session.execute(get_user_query)
    user = dict(user_db.fetchone())
    if not verify_password(body.password, user.get('password')):
        raise HTTPException(status_code=401, detail="Bad email or password")
    id = user.get('id')
    access_token = create_access_token(data={"id": id})
    insert_token_query = update(users_table).where(
       id == users_table.c.id).values(token=access_token)
    await session.execute(insert_token_query)
    await session.commit()
    return access_token


async def delete_token(
        session: AsyncSession,
        token: str
):
    user = await get_user_by_token(
        session=session, token=token
    )
    delete_token_query = update(users_table).where(
        user.get('id') == users_table.c.id).values(token=None)
    await session.execute(delete_token_query)
    await session.commit()
