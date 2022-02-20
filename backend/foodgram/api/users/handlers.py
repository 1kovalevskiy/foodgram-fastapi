from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_field_for_pagination, get_user_from_auth_header
from core.crud import get_user_from_db
from api.users.services import get_user_list, create_user, change_password
from core.exceptions import NotFoundException, ValidationException
from core.settings import ROOT_URL
from db.base import get_session
from schema.user import (UserListResponseSchema, UserResponseSchema,
                         ChangePasswordSchema, UserCreateSchema,
                         UserCreateResponseSchema)

router = APIRouter()


@router.get("/", response_model=UserListResponseSchema)
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
    fields_for_pagination = get_field_for_pagination(
        page=page, limit=limit, count=count, base_url=base_url
    )
    response = UserListResponseSchema(
        results=user_list, **fields_for_pagination
    )
    return response


@router.get("/me", response_model=UserResponseSchema)
async def get_user_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    try:
        user = await get_user_from_auth_header(
            request=request, session=session
        )
    except NotFoundException:
        raise ValidationException()
    return user


@router.post("/set_password", status_code=204)
async def change_password_handler(
        request: Request,
        body: ChangePasswordSchema,
        session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_auth_header(
        request=request, session=session
    )
    await change_password(
        session=session,
        user=user,
        body=body
    )
    return None


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user_handler(
        id: int,
        session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_db(
        session=session, id=id
    )
    return user


@router.post("/", response_model=UserCreateResponseSchema, status_code=201)
async def create_user_handler(
        body: UserCreateSchema,
        session: AsyncSession = Depends(get_session),
):

    user = await create_user(
        session=session, body=body
    )
    response = UserCreateResponseSchema(**user)
    return response

