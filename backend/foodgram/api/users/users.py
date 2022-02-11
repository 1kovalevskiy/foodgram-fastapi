from fastapi import APIRouter, Depends, Request, Body

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlmodel import select

from api.auth.validators import ChangePassword
from api.deps import get_token_from_headers, get_user_by_token
from api.users.services import get_user_list, get_user, create_user, \
    change_password
from api.users.validators import UserResponse, UserUnit, UserCreate
from core.settings import ROOT_URL
from db.base import get_session
from db.schema import users_table

router = APIRouter()


@router.get("/")
async def get_user_list_handler(
        request: Request,
        page: int = 1,
        limit: int = 10,
        session: AsyncSession = Depends(get_session),
):
    user_list, count = await get_user_list(
        page=page, limit=limit, session=session
    )
    base_url = ROOT_URL + request.url.path
    next_url = base_url + f'?page={page+1}&limit={limit}'
    prev_url = base_url + f'?page={page-1}&limit={limit}'
    if page == 1:
        prev_url = None
    if page*limit >= count:
        next_url = None
    response = UserResponse(
        results=user_list, count=count,
        next=next_url, previous=prev_url
    )
    return response


@router.get("/me")
async def get_user_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    token = await get_token_from_headers(request=request)
    user = await get_user_by_token(
        session=session, token=token
    )
    response = UserUnit(**user)
    return response


@router.post("/set_password", status_code=204)
async def change_password_handler(
        request: Request,
        body: ChangePassword,
        session: AsyncSession = Depends(get_session),
):
    token = await get_token_from_headers(request=request)
    user = await get_user_by_token(
        session=session, token=token
    )
    response = await change_password(
        session=session,
        user=user,
        body=body
    )
    return response


@router.get("/{id}")
async def get_user_handler(
        request: Request,
        id: int,
        session: AsyncSession = Depends(get_session),
):
    user = await get_user(
        session=session, id=id
    )
    response = UserUnit(**user)
    return response


@router.post("/", status_code=201)
async def create_user_handler(
        request: Request,
        body: UserCreate,
        session: AsyncSession = Depends(get_session),
):

    user = await create_user(
        session=session, body=body
    )
    response = UserUnit(**user)
    return response

