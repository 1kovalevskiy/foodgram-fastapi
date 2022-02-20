from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (ValidationException, CredentialException,
                             ForbiddenException, NotFoundException)
from db.base import get_session


router = APIRouter()


@router.get("/check_validation_error")
async def check_validation_error_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise ValidationException()


@router.get("/check_credentials_exception")
async def check_credentials_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise CredentialException()


@router.get("/check_forbidden_exception")
async def check_forbidden_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise ForbiddenException()


@router.get("/check_not_found_exception")
async def check_not_found_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise NotFoundException()
