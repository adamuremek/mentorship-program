#!/bin/bash

if [ "$DB" = "postgres" ]
then
    echo "Wating for postgres"

    while ! nc -z -w 1 $DB_HOST $DB_PORT; do
        sleep 1
    done

    echo "Postgres started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"