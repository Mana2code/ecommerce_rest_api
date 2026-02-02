import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.database import Base
from app.config import get_db_path
from app import models

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Use DB_PATH from environment or default
DB_PATH = os.environ.get("DB_PATH") or "./local_data/shop.db"
config.set_main_option("sqlalchemy.url", f"sqlite:///{DB_PATH}")

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
