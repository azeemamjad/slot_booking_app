from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
import sys
import os

# Add backend/ to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your models' Base
from app.db.base import Base  # Make sure app/db/base.py imports all models
from app.core.config import settings

# Alembic Config object
config = context.config

# Use async DB URL directly
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata (for autogenerate)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Handle URL conversion from async to sync
    db_url = config.get_main_option("sqlalchemy.url")
    if db_url.startswith('postgresql+asyncpg://'):
        db_url = db_url.replace('postgresql+asyncpg://', 'postgresql://')

    # Use regular engine instead of async engine for migrations
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():

            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
