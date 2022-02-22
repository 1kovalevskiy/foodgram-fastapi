from sqlalchemy import select, func, Table
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from api.recipes.converters import object_list_from_db_recipe_rows, \
    get_recipes_dict_from_lists
from core.deps import get_user_from_auth_header
from core.exceptions import ValidationException, CredentialException
from db.schema import recipe_table, tag_table, ingredient_table, \
    recipe_tag_table, recipe_ingredient_table, users_table, \
    favorited_recipe_table, shopping_recipe_table
from schema.recipe import RecipeFromDBSchema, RecipeCreateSchema
from schema.user import UserSchema


async def get_recipe_list(
        session: AsyncSession,
        request: Request,
        page: int,
        limit: int,
        is_favorited: int = 0,
        is_in_shopping_cart: int = 0,
        author: int | None = None,
        tags:  list[str] | None = None,
):
    user = None
    try:
        user = await get_user_from_auth_header(request=request, session=session)
    except CredentialException:
        pass
    get_length_query = select([func.count()]).select_from(recipe_table)
    get_length_query, only_favorited, only_in_shopping_cart = filter_query(
        query=get_length_query,
        user=user,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart,
        author=author,
        tags=tags,
    )
    get_length_response = await session.execute(get_length_query)
    count = get_length_response.fetchone()[0]
    if (page - 1) * limit >= count:
        return [], count
    recipe_list = await get_recipes(
        limit=limit, page=page, session=session, user=user, author=author,
        is_favorited=is_favorited, is_in_shopping_cart=is_in_shopping_cart
    )
    return recipe_list, count


async def get_recipes(
        session: AsyncSession,
        page: int,
        limit: int,
        is_favorited: int = 0,
        is_in_shopping_cart: int = 0,
        author: int | None = None,
        user: UserSchema | None = None,
        recipe_id: int | None = None,
        tags: list[str] | None = None,

):
    get_list_query = select(recipe_table, users_table).filter(
        recipe_table.c.author == users_table.c.id
    ).limit(limit).offset((page - 1) * limit)
    if recipe_id:
        get_list_query = get_list_query.where(recipe_table.c.id == recipe_id)
    get_list_query, only_favorited, only_in_shopping_cart = filter_query(
        query=get_list_query,
        user=user,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart,
        author=author,
        tags=tags,
    )
    list_of_recipes_db = await session.execute(get_list_query)
    list_of_recipes = [dict(recipe) for recipe in list_of_recipes_db]
    list_of_recipes_id = [recipe['id'] for recipe in list_of_recipes]

    list_of_relative_ingredients = await get_list_of_relative_ingredients(
        session=session,
        list_of_recipe_id=list_of_recipes_id
    )
    list_of_relative_tags = await get_list_of_relative_tags(
        session=session,
        list_of_recipe_id=list_of_recipes_id
    )

    recipes = get_recipes_dict_from_lists(
        list_of_recipes=list_of_recipes,
        only_favorited=only_favorited,
        only_in_shopping_cart=only_in_shopping_cart,
        list_of_relative_ingredients=list_of_relative_ingredients,
        list_of_relative_tags=list_of_relative_tags
    )
    return recipes


async def get_list_of_relative_ingredients(
        session: AsyncSession,
        list_of_recipe_id: list[int],
):
    get_relative_ingredients_query = select(
        recipe_ingredient_table.c.recipe,
        recipe_ingredient_table.c.amount,
        ingredient_table
    ).filter(
        recipe_ingredient_table.c.recipe.in_(list_of_recipe_id),
        ingredient_table.c.id == recipe_ingredient_table.c.ingredient
    )
    list_of_relative_ingredients_db = await session.execute(
        get_relative_ingredients_query
    )
    list_of_relative_ingredients = [
        ingredient for ingredient in list_of_relative_ingredients_db]
    return list_of_relative_ingredients


async def get_list_of_relative_tags(
        session: AsyncSession,
        list_of_recipe_id: list[int],
):
    get_relative_tags_query = select(
        recipe_tag_table.c.recipe,
        tag_table
    ).filter(
        recipe_tag_table.c.recipe.in_(list_of_recipe_id),
        tag_table.c.id == recipe_tag_table.c.tag
    )
    list_of_relative_tags_db = await session.execute(
        get_relative_tags_query
    )
    list_of_relative_tags = [
        tag for tag in list_of_relative_tags_db]
    return list_of_relative_tags


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
    only_favorited = False
    only_in_shopping_cart = False
    if user and is_favorited == 1:
        user_id = user.id
        query = query.where(
            favorited_recipe_table.c.user == user_id,
            recipe_table.c.id == favorited_recipe_table.c.recipe
        )
        only_favorited = True
    elif is_favorited != 0 or is_favorited != 1:
        ValidationException()
    if user and is_in_shopping_cart == 1:
        user_id = user.id
        query = query.where(
            shopping_recipe_table.c.user == user_id,
            recipe_table.c.id == shopping_recipe_table.c.recipe
        )
        only_in_shopping_cart = True
    elif is_in_shopping_cart != 0 or is_in_shopping_cart != 1:
        ValidationException()
    if author:
        query = query.where(recipe_table.c.author == author)
    if tags:
        query = query.where(
            recipe_table.c.id == recipe_tag_table.c.recipe,
            tag_table.c.id == recipe_tag_table.c.tag,
            tag_table.c.slug.in_(tags)
        )
    return query, only_favorited, only_in_shopping_cart


