from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from schema.recipe import RecipeListResponseSchema, RecipeResponseSchema, \
    RecipeCreateSchema

router = APIRouter()


@router.get("/", response_model=RecipeListResponseSchema)
async def get_recipe_list_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.get("/{id}", response_model=RecipeResponseSchema)
async def get_recipe_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.post("/{id}", response_model=RecipeResponseSchema, status_code=201)
async def create_recipe_handler(
        body: RecipeCreateSchema,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.patch("/{id}", response_model=RecipeResponseSchema)
async def change_recipe_handler(
        body: RecipeCreateSchema,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.delete("/{id}", status_code=204)
async def delete_recipe_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None
