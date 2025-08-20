import os
from alembic import context
from sqlalchemy import create_engine
from models import Base

# Use Docker environment variable
database_url = os.getenv("DATABASE_URL")
target_metadata = Base.metadata

def run_migrations():
    engine = create_engine(database_url)
    with engine.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations()