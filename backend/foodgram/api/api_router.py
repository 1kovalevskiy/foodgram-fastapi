from fastapi import APIRouter

from api.auth import auth
from api.ingredients import ingredients
from api.users import users

api_router = APIRouter()
api_router.include_router(
    ingredients.router, prefix="/ingredients", tags=["ingredients"]
)
api_router.include_router(
    users.router, prefix="/users", tags=["users"]
)
api_router.include_router(
    auth.router, prefix="/auth", tags=["auth"]
)

