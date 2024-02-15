#!/bin/bash

# Check if postgres is being used
if [ "$DB" = "postgres" ]
then
    echo "Wating for postgres"

    # Wait for postgres to become available
    while ! nc -z -w 1 $DB_HOST $DB_PORT; do
        sleep 1
    done

    echo "Postgres started"
fi

# Reset the db and apply migrations
# python manage.py reset_db --router=default --noinput --close-sessions
# python manage.py migrate

if [ "$DEBUG" != 1 ]
then
    echo "Collecting static files"

    python manage.py collectstatic --no-input --clear
    
    echo "Done collecting static"
fi

# Execute the default docker cmd or one passed to the entrypoint script
exec "$@"