#!/bin/bash

# Wait for postgres to be ready
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
python manage.py migrate

# Load initial data (fixtures)
python manage.py loaddata activities/fixtures/activity_types.json

# Start server
exec "$@"