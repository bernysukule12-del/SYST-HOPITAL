#!/bin/sh
set -e

echo "Starting entrypoint..."

if [ "${DATABASE}" = "postgres" ]; then
  echo "Waiting for postgres at ${SQL_HOST}:${SQL_PORT}..."
  while ! nc -z ${SQL_HOST} ${SQL_PORT}; do
    sleep 0.1
  done
fi

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Collect static files"
python manage.py collectstatic --noinput

exec "$@"
