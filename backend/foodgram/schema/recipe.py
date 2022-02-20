from pydantic import BaseModel, constr, AnyHttpUrl, conint, Field, EmailStr
from pydantic.color import Color

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
    image: str
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


class RecipeFromDBSchema(BaseModel):
    id: int
    # author: int
    name: constr(max_length=255)
    image: str
    text: str
    cooking_time: conint(gt=0)
    tag_id: int = Field(alias="id_1")
    tag_name: constr(max_length=255) = Field(alias="name_1")
    tag_slug: constr(max_length=255) = Field(alias="slug")
    tag_color: Color = Field(alias="color")
    ingredient_id: int = Field(alias="id_2")
    ingredient_name: constr(max_length=255) = Field(alias="name_2")
    ingredient_measurement_unit: constr(max_length=255) = Field(
        alias="measurement_unit")
    ingredient_amount: conint(gt=0) = Field(alias="amount")
    user_id: int = Field(alias="id_3")
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    is_subscribed: bool = False
