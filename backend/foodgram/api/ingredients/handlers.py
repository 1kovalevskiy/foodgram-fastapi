from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.ingredient import IngredientResponseSchema

router = APIRouter()


@router.get("/", response_model=list[IngredientResponseSchema | None])
async def get_ingredient_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.get('/{id}', response_model=IngredientResponseSchema)
async def get_ingredient_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None
