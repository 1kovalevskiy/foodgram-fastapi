from pydantic import BaseModel, constr, AnyHttpUrl


class FavoriteResponseSchema(BaseModel):
    id: int
    name: constr(max_length=255)
    image: AnyHttpUrl
    cooking_time: int