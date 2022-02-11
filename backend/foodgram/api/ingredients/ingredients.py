from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.base import get_session

router = APIRouter()


@router.get("/")
async def get_ingredient_list(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(text("SELECT 1"))
    response = result.all()[0][0]
    return {"message": response}


@router.get("/{id}")
async def get_ingredient_detail():
    return {"message": "Hello World"}