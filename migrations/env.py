import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import pool, create_engine, engine_from_config
from alembic import context
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

from app.db.models.user import User
from app.db.models.product import Product
from app.db.models.order import Order
from app.db.models.cart_item import CartItem
from app.db.models.category import Category

# Налаштування логування
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Використовуємо всі метадані моделей
target_metadata = Base.metadata


# Створюємо **синхронний** engine для Alembic (бо async не підтримується)
# def get_sync_engine():
#     return engine_from_config(
#         {
#             "sqlalchemy.url": settings.DATABASE_URL,
#         },
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Функція для запуску міграцій в "offline" режимі
# async def run_migrations_offline() -> None:
#     # url = settings.DATABASE_URL
#     context.configure(
#         url=settings.DATABASE_URL,
#         # url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )
#
#     with context.begin_transaction():
#         context.run_migrations()
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Функція для запуску міграцій в "online" режимі
# async def run_migrations_online() -> None:
#     engine = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
#
#     async with engine.begin() as conn:
#         await conn.run_sync(do_run_migrations)
#
#     await engine.dispose()
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
# First GPT Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Функція для запуску міграцій в "online" режимі
# engine = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# def run_migrations_online():
#     # Синхронно виконуємо міграції
#     with engine.connect() as conn:
#         context.configure(connection=conn, target_metadata=target_metadata)
#         with context.begin_transaction():
#             context.run_migrations()
# -----------------------------------------------------------------------
# def run_migrations_online() -> None:
#     """Запуск міграцій у онлайн-режимі."""
#     connectable = get_sync_engine()
#
#     with connectable.connect() as connection:
#         context.configure(connection=connection, target_metadata=target_metadata)
#         with context.begin_transaction():
#             context.run_migrations()
# -----------------------------------------------------------------------
# async_engine = create_async_engine(settings.DATABASE_URL, future=True)
# def do_run_migrations(connection):
#     """Синхронний запуск міграцій у контексті Alembic"""
#     context.configure(connection=connection, target_metadata=target_metadata)
#     with context.begin_transaction():
#         context.run_migrations()
#
# async def run_migrations():
#     """Асинхронне виконання міграцій"""
#     async with async_engine.connect() as connection:
#         await connection.run_sync(do_run_migrations)
#
# def run_migrations_online():
#     """Запускає міграції в асинхронному режимі"""
#     asyncio.run(run_migrations())
#
# run_migrations_online()
# -----------------------------------------------------------------------
sync_engine = create_engine(settings.SYNC_DATABASE_URL, poolclass=pool.NullPool)
def run_migrations_offline():
    """Запуск міграцій у офлайн-режимі."""
    context.configure(
        url=settings.SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online():
    """Запуск міграцій у онлайн-режимі."""
    with sync_engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
# -----------------------------------------------------------------------

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Запускаємо міграції для поточного підключення
# async def do_run_migrations(connection: AsyncConnection):
#     context.configure(connection=connection, target_metadata=target_metadata)
#
#     with context.begin_transaction():
#         context.run_migrations()
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# First GPT Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Функція для запуску міграцій
# async def do_run_migrations(connection: AsyncConnection):
#     # Використовуємо sync_connection для налаштування Alembic
#     sync_connection = connection.sync_connection
#     context.configure(connection=sync_connection, target_metadata=target_metadata)
#
#     with context.begin_transaction():
#         context.run_migrations()
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
    # asyncio.run(run_migrations_online())
    # run_migrations_online()

#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
# First GPT Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# def run():
#     if context.is_offline_mode():
#         asyncio.run(run_migrations_offline())
#     else:
#         asyncio.run(run_migrations_online())
# run()
# -----------------------------------------------------------------------