# What: A startup script for our container. It first waits for the database to be ready, then runs our database migrations, and finally starts the web server.
# Why: This solves a common race condition where the backend container starts before the database is ready to accept connections. This script ensures a smooth and orderly startup sequence every time.

#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
# Use pg_isready to check if the database is accepting connections
until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
  sleep 1
done
echo "PostgreSQL started"

echo "Running database migrations..."
# Navigate to the app directory where alemnic.ini is located
cd /app
alembic -c alembic.ini upgrade head

echo "Starting application..."
# Execute the command passed to the script (e.g., uvicorn)
exec "$@"