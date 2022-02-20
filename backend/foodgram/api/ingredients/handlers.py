from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.ingredients.services import get_ingredient_list, get_ingredient
from db.base import get_session
from schema.ingredient import IngredientResponseSchema

router = APIRouter()


@router.get("/", response_model=list[IngredientResponseSchema | None])
async def get_ingredient_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
        name: str | None = None,
):
    response = await get_ingredient_list(
        name=name, session=session
    )
    return response


@router.get('/{id}', response_model=IngredientResponseSchema)
async def get_ingredient_handler(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    response = await get_ingredient(
        id=id, session=session
    )
    return response
