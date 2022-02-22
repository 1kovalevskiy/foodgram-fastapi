from pydantic import BaseModel, constr, conint

from schema.recipe import IngredientResponseObject, RecipeResponseSchema
from schema.tag import TagResponseSchema
from schema.user import UserResponseSchema


def object_list_from_db_recipe_rows(rows: list):
    res_dict = {}
    for row in rows:
        tag = TagResponseSchema(
            id=row.tag_id,
            name=row.tag_name,
            color=row.tag_color,
            slug=row.tag_slug
        )
        ingredient = IngredientResponseObject(
            id=row.ingredient_id,
            name=row.ingredient_name,
            measurement_unit=row.ingredient_measurement_unit,
            amount=row.ingredient_amount
        )
        if res_dict.get(row.id) is None:
            res_dict[row.id] = RecipeResponseSchema(
                id=row.id,
                name=row.name,
                text=row.text,
                image=row.image,
                cooking_time=row.cooking_time,
                author=UserResponseSchema(
                    id=row.user_id,
                    username=row.username,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    email=row.email
                ),
                tags=[
                    tag
                ],
                ingredients=[
                    ingredient
                ]
            )
        else:
            if tag.id not in [tagx.id for tagx in res_dict[row.id].tags]:
                res_dict[row.id].tags.append(tag)
            if ingredient.id not in [ingredientx.id for ingredientx in
                                  res_dict[row.id].ingredients]:
                res_dict[row.id].ingredients.append(ingredient)
    return list(res_dict.values())


class RecipeSchema(BaseModel):
    id: int
    tags: list[TagResponseSchema | None]
    author: UserResponseSchema
    ingredients: list[IngredientResponseObject | None]
    is_favorited: bool = False
    is_in_shopping_cart: bool = False
    name: constr(max_length=255)
    image: str
    text: str
    cooking_time: conint(gt=0)


def get_recipes_dict_from_lists(
        list_of_recipes: list,
        list_of_relative_ingredients: list,
        list_of_relative_tags: list,
        only_favorited: bool,
        only_in_shopping_cart: bool
):
    recipes = {}
    for recipe in list_of_recipes:
        author = UserResponseSchema(
            id=recipe.get('id_1'),
            username=recipe.get('username'),
            first_name=recipe.get('first_name'),
            last_name=recipe.get('last_name'),
            email=recipe.get('email'),
            is_subscribed = False
        )
        recipes[recipe['id']] = RecipeSchema(
            id=recipe['id'],
            name=recipe['name'],
            text=recipe['text'],
            image=recipe['image'],
            cooking_time=recipe['cooking_time'],
            author=author,
            is_favorited=only_favorited,
            is_in_shopping_cart=only_in_shopping_cart,
            tags=[],
            ingredients=[]
        )
    for ingredient_ in list_of_relative_ingredients:
        ingredient = IngredientResponseObject(**ingredient_)
        recipes[ingredient_['recipe']].ingredients.append((ingredient))
    for tag_ in list_of_relative_tags:
        tag = TagResponseSchema(**tag_)
        recipes[tag_['recipe']].tags.append((tag))
    return list(recipes.values())