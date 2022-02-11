from pydantic import (BaseModel, EmailStr, constr)


class LoginData(BaseModel):
    email: EmailStr
    password: constr(max_length=255)


class User:
    id: int
    username: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    is_subscribed: bool
    password: constr(max_length=255)


class Token(BaseModel):
    token: str


class ChangePassword(BaseModel):
    new_password: constr(max_length=255)
    current_password: constr(max_length=255)
