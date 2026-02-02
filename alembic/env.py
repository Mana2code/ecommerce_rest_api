import sys, os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import Base
from app import models
from app.config import get_db_path

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Docker DB path (fallback to local if needed)
DB_PATH = os.environ.get("DB_PATH") or get_db_path()
SQLALCHEMY_URL = f"sqlite:///{DB_PATH}"


def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=SQLALCHEMY_URL,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
