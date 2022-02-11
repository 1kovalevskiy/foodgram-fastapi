from types import NoneType

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.services import check_user_data, delete_token
from api.deps import get_token_from_headers
from api.auth.validators import LoginData, Token
from api.exceptions import credentials_exception
from db.base import get_session

router = APIRouter()


@router.post("/token/login/")
async def get_user_list_handler(
        request: Request,
        body: LoginData,
        session: AsyncSession = Depends(get_session),
):
    token = await check_user_data(
        session=session, body=body
    )
    response = Token(token=token)
    return response


@router.post("/token/logout/", status_code=204)
async def get_user_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    token = await get_token_from_headers(request=request)
    await delete_token(session=session, token=token)
    return
