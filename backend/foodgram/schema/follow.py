from pydantic import BaseModel, constr, EmailStr, AnyHttpUrl


class RecipeObject(BaseModel):
    id: int
    name: constr(max_length=255)
    image: AnyHttpUrl
    cooking_time: int


class FollowResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    is_subscribed: bool = False
    recipes: list[RecipeObject | None]
    recipes_count: int


class FollowListResponseSchema(BaseModel):
    count: int
    next: AnyHttpUrl | None
    previous: AnyHttpUrl | None
    results: list[FollowResponseSchema | None]