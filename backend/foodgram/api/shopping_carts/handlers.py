from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.buy_list import BuyCartResponseSchema

router = APIRouter()


@router.get('/download_shopping_cart')
async def download_shopping_cart_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.post(
    "/{id}/shopping_cart", response_model=BuyCartResponseSchema, status_code=201
)
async def add_recipe_in_shopping_cart_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.delete('/{id}/shopping_cart', status_code=204)
async def delete_recipe_in_shopping_cart_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None