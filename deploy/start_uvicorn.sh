#!/bin/sh

# Применение миграций Alembic
echo "Applying database migrations..."
if ! alembic upgrade head; then
    echo "Alembic migrations failed. Exiting."
    exit 1
fi
echo "Migrations applied successfully."

# Запуск Uvicorn с exec для передачи сигналов
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
