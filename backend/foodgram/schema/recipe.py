from pydantic import BaseModel, constr, AnyHttpUrl, conint

from schema.ingredient import IngredientResponseSchema
from schema.tag import TagResponseSchema
from schema.user import UserResponseSchema


class IngredientResponseObject(IngredientResponseSchema):
    amount: conint(gt=0)


class RecipeResponseSchema(BaseModel):
    id: int
    tags: list[TagResponseSchema]
    author: UserResponseSchema
    ingredients: list[IngredientResponseObject]
    is_favorited: bool = False
    is_in_shopping_cart: bool = False
    name: constr(max_length=255)
    image: AnyHttpUrl
    text: str
    cooking_time: conint(gt=0)


class IngredientCreateObject(BaseModel):
    id: int
    amount: conint(gt=0)


class RecipeCreateSchema(BaseModel):
    tags: list[int]
    ingredients: list[IngredientCreateObject]
    name: constr(max_length=255)
    image: str
    text: str
    cooking_time: conint(gt=0)


class RecipeListResponseSchema(BaseModel):
    count: int
    next: AnyHttpUrl | None
    previous: AnyHttpUrl | None
    results: list[RecipeResponseSchema | None]