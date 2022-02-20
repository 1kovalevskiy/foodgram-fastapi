from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.tags.services import get_tag_list, get_tag
from db.base import get_session
from schema.tag import TagResponseSchema

router = APIRouter()


@router.get("/", response_model=list[TagResponseSchema | None])
async def get_tag_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    response = await get_tag_list(
        session=session
    )
    return response


@router.get('/{id}', response_model=TagResponseSchema)
async def get_tag_handler(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    response = await get_tag(
        id=id, session=session
    )
    return response
