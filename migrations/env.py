import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import pool
from alembic import context

from app.core.config import settings
from app.db.base import Base  # імпортуємо базовий клас моделей

# Налаштування логування
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Використовуємо всі метадані моделей
target_metadata = Base.metadata

# Функція для запуску міграцій в "offline" режимі
def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Функція для запуску міграцій в "online" режимі
async def run_migrations_online() -> None:
    engine = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()

# Запускаємо міграції для поточного підключення
def do_run_migrations(connection: AsyncConnection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
