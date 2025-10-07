# The Alembic script that is run when we use the alembic command.
# What: This script programmatically configures Alembic. Critically, it imports our application's settings and database models.
# Why: By importing our Base object (which our models inherit from), Alembic can automatically detect changes to our models and generate migration scripts for us. It also ensures that migrations are run against the correct database as defined in our .env file, not a hardcoded URL.

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add the parent directory to the Python path so we can import backend
# sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# this is alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Import your models here so that they are available to Alembic
# for autogeneration of migrations.
from app.database import Base
from app.config import settings
from app.models.database.audit import AuditLog
from app.models.database.patient import Patient
from app.models.database.user import User
from app.models.database.study import DICOMStudy

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable here
    as well. By skipping the Engine creation we don't even
    need a DBAPI to be available. Calls to context.execute()
    here emit the given string to the string to the script output.
    """


    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    from app.database import engine

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
