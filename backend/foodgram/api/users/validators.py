from typing import List
from pydantic import (BaseModel, ValidationError, validator, root_validator,
                      constr, StrictStr, Field, EmailStr, AnyHttpUrl)


class UserUnit(BaseModel):
    id: int
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    is_subscribed: bool = False


class UserCreate(BaseModel):
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    password: constr(max_length=255)


class UserResponse(BaseModel):
    count: int
    next: AnyHttpUrl | None
    previous: AnyHttpUrl | None
    results: List[UserUnit | None]
