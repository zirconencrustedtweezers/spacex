#!/bin/bash
echo "Starting spaceX Backend..."

echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U admin; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

echo "PostgreSQL is ready!"

echo "Running database migrations..."
alembic upgrade head

echo "Migrations completed!"

echo "Starting FastAPI server..."
exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload
