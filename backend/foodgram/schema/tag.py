from pydantic import BaseModel, constr
from pydantic.color import Color


class TagResponseSchema(BaseModel):
    id: int
    name: constr(max_length=255)
    color: Color
    slug: constr(max_length=255)
