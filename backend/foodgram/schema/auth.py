from pydantic import BaseModel, constr, EmailStr


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: constr(max_length=255)


class LoginResponseSchema(BaseModel):
    auth_token: str
