from fastapi import APIRouter

from api.auth import handlers as auth_handlers
from api.favorites import handlers as favorites_handlers
from api.follows import handlers as follows_handlers
from api.ingredients import handlers as ingredients_handlers
from api.recipes import handlers as recipes_handlers
from api.shopping_carts import handlers as shopping_carts_handlers
from api.tags import handlers as tags_handlers
from api.users import handlers as users_handlers
from api.checks import handlers as checks_handlers

api_router = APIRouter()


api_router.include_router(
    tags_handlers.router, prefix="/tags", tags=["tags"]
)
api_router.include_router(
    recipes_handlers.router, prefix="/recipes", tags=["recipes"]
)
api_router.include_router(
    follows_handlers.router, prefix="/users", tags=["follows"]
)
api_router.include_router(
    favorites_handlers.router, prefix="/favorites", tags=["favorites"]
)
api_router.include_router(
    ingredients_handlers.router, prefix="/ingredients", tags=["ingredients"]
)
api_router.include_router(
    users_handlers.router, prefix="/users", tags=["users"]
)
api_router.include_router(
    auth_handlers.router, prefix="/auth", tags=["auth"]
)
api_router.include_router(
    shopping_carts_handlers.router,
    prefix="/shopping_carts",
    tags=["shopping_carts"]
)
api_router.include_router(
    checks_handlers.router, prefix="/checks", tags=["checks"]
)
