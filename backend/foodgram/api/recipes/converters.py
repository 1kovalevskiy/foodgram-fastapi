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