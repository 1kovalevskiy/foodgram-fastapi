from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.services import create_token, delete_token
from core.deps import get_token_from_headers
from db.base import get_session
from schema.auth import LoginResponseSchema, LoginRequestSchema

router = APIRouter()


@router.post(
    "/token/login/", response_model=LoginResponseSchema, status_code=201
)
async def login_handler(
        body: LoginRequestSchema,
        session: AsyncSession = Depends(get_session),
):
    token = await create_token(
        session=session, body=body
    )
    return token


@router.post("/token/logout/", status_code=204)
async def logout_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    token = await get_token_from_headers(request=request)
    await delete_token(session=session, token=token)
    return
