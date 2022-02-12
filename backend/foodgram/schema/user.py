from pydantic import BaseModel, constr, EmailStr, AnyHttpUrl


class UserSchema(BaseModel):
    id: int
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    is_subscribed: bool = False
    password: str
    token: str | None


class UserResponseSchema(BaseModel):
    id: int
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    is_subscribed: bool = False


class UserCreateSchema(BaseModel):
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    password: constr(max_length=255)


class UserCreateResponseSchema(BaseModel):
    id: int
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr


class UserListResponseSchema(BaseModel):
    count: int
    next: AnyHttpUrl | None
    previous: AnyHttpUrl | None
    results: list[UserResponseSchema | None]


class ChangePasswordSchema(BaseModel):
    new_password: constr(max_length=255)
    current_password: constr(max_length=255)