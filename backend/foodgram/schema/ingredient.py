from pydantic import BaseModel, constr


class IngredientResponseSchema(BaseModel):
    id: int
    name: constr(max_length=255)
    measurement_unit: constr(max_length=255)
