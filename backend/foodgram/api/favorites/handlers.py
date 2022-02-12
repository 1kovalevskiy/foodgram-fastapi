from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.favorite import FavoriteResponseSchema

router = APIRouter()


@router.post(
    "/{id}/favorite", response_model=FavoriteResponseSchema, status_code=201
)
async def add_recipe_in_favorite_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.delete('/{id}/favorite', status_code=204)
async def delete_recipe_in_favorite_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None