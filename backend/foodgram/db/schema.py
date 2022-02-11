import datetime
from enum import Enum, unique
from sqlalchemy import (
    Column, Date, Enum as PgEnum, ForeignKey, ForeignKeyConstraint, Integer,
    String, Table, MetaData, UniqueConstraint, CheckConstraint, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
import uuid

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('username', String, nullable=False, index=True, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('password', String, nullable=False),
    Column('token', String)
)


follows_table = Table(
    'follows',
    metadata,
    Column('user', Integer, primary_key=True),
    Column('author', Integer, primary_key=True),
    ForeignKeyConstraint(('user',), ('users.id',)),
    ForeignKeyConstraint(('author',), ('users.id',)),
    UniqueConstraint('user', 'author'),
)


tag_table = Table(
    'tags',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('name', String, nullable=False, unique=True),
    Column('color', String, nullable=False),
    Column('slug', String, nullable=False, index=True, unique=True)
)


ingredient_table = Table(
    'ingredients',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('measurement_unit', String, nullable=False)
)


recipe_table = Table(
    'recipes',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('text', String, nullable=False),
    Column('cooking_time', Integer, nullable=False),
    Column('image', String, nullable=False),
    Column('author', Integer, primary_key=True),
    ForeignKeyConstraint(('author',), ('users.id',)),
    Column('pub_date', DateTime, default=datetime.datetime.utcnow)
)


recipe_ingredient_table = Table(
    'recipe_ingredients',
    metadata,
    Column('recipe', Integer, primary_key=True),
    Column('ingredient', Integer, primary_key=True),
    Column('amount', Integer, nullable=False),
    ForeignKeyConstraint(('recipe',), ('recipes.id',)),
    ForeignKeyConstraint(('ingredient',), ('ingredients.id',)),
    UniqueConstraint('recipe', 'ingredient'),
)


recipe_tag_table = Table(
    'recipe_tags',
    metadata,
    Column('recipe', Integer, primary_key=True),
    Column('tag', Integer, primary_key=True),
    ForeignKeyConstraint(('recipe',), ('recipes.id',)),
    ForeignKeyConstraint(('tag',), ('tags.id',)),
    UniqueConstraint('recipe', 'tag'),
)


favorited_recipe_table = Table(
    'favorited_recipes',
    metadata,
    Column('user', Integer, primary_key=True),
    Column('recipe', Integer, primary_key=True),
    ForeignKeyConstraint(('recipe',), ('recipes.id',)),
    ForeignKeyConstraint(('user',), ('users.id',)),
    UniqueConstraint('recipe', 'user'),
)


shopping_recipe_table = Table(
    'shopping_recipes',
    metadata,
    Column('user', Integer, primary_key=True),
    Column('recipe', Integer, primary_key=True),
    ForeignKeyConstraint(('recipe',), ('recipes.id',)),
    ForeignKeyConstraint(('user',), ('users.id',)),
    UniqueConstraint('recipe', 'user'),
)
