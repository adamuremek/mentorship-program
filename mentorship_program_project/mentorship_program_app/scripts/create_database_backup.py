"""
FILE NAME: create_database_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script that creates a backup of the database to ../DATABASE_BACKUPS 
or another file specified in the .env file under DB_BACKUP_PATH.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> python manage.py runscript create_database_backup
"Backup created successfully: [FULL_PATH]\mentorship-program\mentorship_program_project\DATABASE_BACKUPS\mentorship_app_2024-04-09_23-20-06.sql"

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT

"""

import subprocess
import urllib.parse
from datetime import datetime
import os

def run():
    try:
        str_time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"{os.environ.get('DB_NAME')}_{str_time_stamp}.sql"
        backup_file_path = f"{os.path.abspath(os.environ.get('DB_BACKUP_PATH'))}/{backup_file}"

        str_encoded_password = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))

        command = [
            'pg_dump',
            f'--dbname=postgresql://{os.environ.get("DB_USER")}:{str_encoded_password}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}',
            f'--file={backup_file_path}'
        ]

        #Send it
        subprocess.run(command, check=True)


        print(f"Backup created successfully: {os.path.abspath(backup_file_path)}")
    except subprocess.CalledProcessError as e :
        print(f"Error: Failed to create backup - {e}")
    except Exception as e:
        print(f"Error: {e}")
