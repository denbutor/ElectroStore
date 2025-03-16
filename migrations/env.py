import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import pool, create_engine
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

# Функція для запуску міграцій в "offline" режимі
async def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Функція для запуску міграцій в "online" режимі
async def run_migrations_online() -> None:
    engine = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()
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

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# Запускаємо міграції для поточного підключення
async def do_run_migrations(connection: AsyncConnection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()
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

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
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