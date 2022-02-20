from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from api.recipes.converters import object_list_from_db_recipe_rows
from core.deps import get_user_from_auth_header
from core.exceptions import ValidationException, CredentialException
from db.schema import recipe_table, tag_table, ingredient_table, \
    recipe_tag_table, recipe_ingredient_table, users_table
from schema.recipe import RecipeFromDBSchema, RecipeCreateSchema
from schema.user import UserSchema


async def get_recipe_list(
        request: Request,
        page: int,
        limit: int,
        is_favorited: int,
        is_in_shopping_cart: int,
        author: int | None,
        tags:  list[str] | None,
        session: AsyncSession
):
    user = None
    try:
        user = await get_user_from_auth_header(
                request=request, session=session
            )
    except CredentialException:
        pass
    get_length_query = select([func.count()]).select_from(recipe_table)

    get_length_response = await session.execute(get_length_query)
    count = get_length_response.fetchone()[0]
    if (page - 1) * limit >= count:
        return [], count
    recipe_list = await get_recipes(
        limit=limit, page=page, session=session
    )
    recipe_list = recipe_list[((page - 1) * limit):(page * limit)]
    return recipe_list, count


async def get_recipes(
        session: AsyncSession,
        page: int | None = None,
        limit: int | None = None,
        id: int | None = None,
):
    get_list_query = select(
        recipe_table,
        tag_table,
        ingredient_table,
        recipe_ingredient_table.c.amount,
        users_table
    ).filter(
        recipe_table.c.id == recipe_tag_table.c.recipe,
        tag_table.c.id == recipe_tag_table.c.tag
    ).filter(
        recipe_table.c.id == recipe_ingredient_table.c.recipe,
        ingredient_table.c.id == recipe_ingredient_table.c.ingredient
    ).filter(
        recipe_table.c.author == users_table.c.id
    )
    # if limit and page:
    #     get_list_query = get_list_query.limit(limit).offset((page - 1) * limit)
    if id:
        get_list_query = get_list_query.where(recipe_table.c.id == id)
    get_list_response = await session.execute(get_list_query)
    res = [RecipeFromDBSchema(**dict(recipe)) for recipe in get_list_response]
    return object_list_from_db_recipe_rows(res)


async def create_recipe(
        body: RecipeCreateSchema,
        request: Request,
        session: AsyncSession
):
    user = await get_user_from_auth_header(
        request=request, session=session
    )
    create_recipe = recipe_table.insert().values(
        name=body.name,
        text=body.text,
        cooking_time=body.cooking_time,
        image=body.image,
        author=user.id
    )
    curs = await session.execute(create_recipe)
    recipe_id = curs.inserted_primary_key[0]
    create_tags = recipe_tag_table.insert().values(
        [{"recipe": recipe_id, "tag": tag_id} for tag_id in body.tags]
    )
    curs = await session.execute(create_tags)
    create_ingredients = recipe_ingredient_table.insert().values(
        [{"recipe": recipe_id, "ingredient": ingredient.id,
          "amount": ingredient.amount} for ingredient
         in body.ingredients]
    )
    curs = await session.execute(create_ingredients)
    await session.commit()
    result = await get_recipes(session=session, id=recipe_id)
    return result[0]



def filter_query(
    query: select,
    user: UserSchema | None,
    is_favorited: int,
    is_in_shopping_cart: int,
    author: int | None,
    tags: list[str] | None,
):

    if is_favorited == 1:
        pass
    elif is_favorited != 0 or is_favorited != 1:
        ValidationException()
    if is_in_shopping_cart == 1:
        pass
    elif is_in_shopping_cart != 0 or is_in_shopping_cart != 1:
        ValidationException()
    if author:
        query = query.where(recipe_table.c.author == author)
    if tags:
        query = query.where(
            recipe_table.c.id == recipe_tag_table.c.recipe,
            tag_table.c.id == recipe_tag_table.c.tag
        ).where(tag_table.c.slug.in_(tags))
    return query


