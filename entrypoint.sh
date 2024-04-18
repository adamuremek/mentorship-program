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

if [ "$DEBUG" != 1 ]
then
    echo "Collecting static files"

    python /mentorship_program/mentorship_program_project/manage.py collectstatic --no-input --clear
    
    echo "Done collecting static"
fi

# Copy default media files into the media directory
mkdir -p $MEDIA_ROOT
cp -r /mentorship_program/mentorship_program_project/media/* $MEDIA_ROOT

mkdir -p $BACKUP_ROOT

# Execute the default docker cmd or one passed to the entrypoint script
exec "$@"