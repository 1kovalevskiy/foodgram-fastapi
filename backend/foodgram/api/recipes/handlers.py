from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.recipes.services import get_recipe_list, create_recipe
from core.deps import get_field_for_pagination
from core.settings import ROOT_URL
from db.base import get_session
from schema.recipe import RecipeListResponseSchema, RecipeResponseSchema, \
    RecipeCreateSchema

router = APIRouter()


@router.get("/", response_model=RecipeListResponseSchema)
async def get_recipe_list_handler(
        request: Request,
        page: int = 1,
        limit: int = 10,
        is_favorited: int = 0,
        is_in_shopping_cart: int = 0,
        author: int | None = None,
        tags: list[str] | None = Query(None),
        session: AsyncSession = Depends(get_session),
):
    recipe_list, count = await get_recipe_list(
        page=page, limit=limit, is_favorited=is_favorited, author=author,
        is_in_shopping_cart=is_in_shopping_cart, tags=tags, session=session,
        request=request
    )
    base_url = ROOT_URL + request.url.path
    fields_for_pagination = get_field_for_pagination(
        page=page, limit=limit, count=count, base_url=base_url
    )
    response = RecipeListResponseSchema(
        results=recipe_list, **fields_for_pagination
    )
    return response


@router.get("/{id}", response_model=RecipeResponseSchema)
async def get_recipe_handler(
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return None


@router.post("/", response_model=RecipeResponseSchema, status_code=201)
async def create_recipe_handler(
        body: RecipeCreateSchema,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    result = await create_recipe(
        body=body, request=request, session=session
    )
    return result


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
