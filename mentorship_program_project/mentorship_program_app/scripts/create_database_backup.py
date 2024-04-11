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
import tarfile

def run():
    """
    Description
    -----------
    Dumps the database to a place specified by DB_BACKUP_PATH in .env

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - An integer exit code 0 for success or 1 for failure.

    Example Usage
    -------------

    >>> python manage.py runscript create_database_backup
    "Backup created successfully: [FULL_PATH]\mentorship-program\mentorship_program_project\DATABASE_BACKUPS\mentorship_app_2024-04-09_23-20-06.sql"

    Authors
    -------
    Justin Goupil
    """

    try:
        str_time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"{os.environ.get('DB_NAME')}_{str_time_stamp}.sql"
        backup_file_path = f"{os.path.abspath(os.environ.get('DB_BACKUP_PATH'))}/{backup_file}"
        tarball_path = f"{backup_file_path}.tar.gz"

        if not os.path.exists(os.path.abspath(os.environ.get('DB_BACKUP_PATH'))):
            raise FileNotFoundError(f"The directory does not exist: {os.path.abspath(os.environ.get('DB_BACKUP_PATH'))}")

        str_encoded_password = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))

        command = [
            'pg_dump',
            f'--dbname=postgresql://{os.environ.get("DB_USER")}:{str_encoded_password}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}',
            f'--file={backup_file_path}'
        ]

        #Send it
        subprocess.run(command, check=True)

        try:
            # Create tarball
            with tarfile.open(tarball_path, 'x:gz') as tar:
                tar.add(backup_file_path, arcname=os.path.basename(backup_file_path))
        except FileExistsError as e:
            #This should never happen, but just in case it does.
            print(f"This file already exists: {backup_file_path}\nError: {e}\n")

        #Remove the uncompressed file
        os.remove(backup_file_path)


        print(f"Backup created successfully: {os.path.abspath(tarball_path)}")
        return 0
    except subprocess.CalledProcessError as e :
        str_error_msg = f"Error: Failed to create backup - {e}"

        print(str_error_msg)
        return 1
    except Exception as e:
        str_error_msg = f"Error: {e}"

        print(str_error_msg)
        return 1