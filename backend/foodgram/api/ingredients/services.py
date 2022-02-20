from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from db.schema import ingredient_table
from schema.ingredient import IngredientResponseSchema


async def get_ingredient_list(
        name: str | None,
        session: AsyncSession,
):
    query = select(ingredient_table)
    if name:
        query = query.where(ingredient_table.c.name.contains(name))
    ingredients_db = await session.execute(query)
    ingredient_list = [IngredientResponseSchema(**dict(ingredient))
                       for ingredient in ingredients_db]
    return ingredient_list


async def get_ingredient(
        id:int,
        session: AsyncSession,
):
    query = select(ingredient_table).where(ingredient_table.c.id == id)
    ingredient_db = await session.execute(query)
    ingredient = ingredient_db.fetchone()
    if ingredient is None:
        raise NotFoundException()
    return IngredientResponseSchema(**dict(ingredient))