import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importa Base y engine de tu proyecto
from Proyecto3.database import Base, engine

# Configuración del logging
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

# Agrega tu metadata a la variable target_metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Corre las migraciones en modo offline."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Corre las migraciones en modo online."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Llama a la función adecuada según el modo de ejecución
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
