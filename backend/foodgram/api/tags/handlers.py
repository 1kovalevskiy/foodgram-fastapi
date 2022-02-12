from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.tag import TagResponseSchema

router = APIRouter()


@router.get("/", response_model=list[TagResponseSchema | None])
async def get_tag_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.get('/{id}', response_model=TagResponseSchema)
async def get_tag_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None
