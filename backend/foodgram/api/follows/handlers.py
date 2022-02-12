from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.follow import FollowListResponseSchema, FollowResponseSchema

router = APIRouter()


@router.get("/subscriptions", response_model=FollowListResponseSchema)
async def get_subscriptions_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.post(
    '/{id}/subscribe', response_model=FollowResponseSchema, status_code=201
)
async def subscribe_to_user_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.delete('/{id}/subscribe', status_code=204)
async def unsubscribe_to_user_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None
