from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException
from db.schema import tag_table
from schema.tag import TagResponseSchema


async def get_tag_list(
        session: AsyncSession,
):
    query = select(tag_table)
    tags_db = await session.execute(query)
    tag_list = [TagResponseSchema(**dict(tag)) for tag in tags_db]
    return tag_list


async def get_tag(
        id: int,
        session: AsyncSession,
):
    query = select(tag_table).where(tag_table.c.id == id)
    tag_db = await session.execute(query)
    tag = tag_db.fetchone()
    if tag is None:
        raise NotFoundException()
    return TagResponseSchema(**dict(tag))