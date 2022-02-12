from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (validations_exception, credentials_exception,
                             forbidden_exception, not_found_exception)
from db.base import get_session


router = APIRouter()


@router.get("/check_validation_error")
async def check_validation_error_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise validations_exception()


@router.get("/check_credentials_exception")
async def check_credentials_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise credentials_exception()


@router.get("/check_forbidden_exception")
async def check_forbidden_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise forbidden_exception()


@router.get("/check_not_found_exception")
async def check_not_found_exception_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    raise not_found_exception()
