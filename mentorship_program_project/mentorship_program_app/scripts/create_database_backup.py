"""
FILE NAME: create_database_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script that creates a backup of the database to ../DATABASE_BACKUPS 
or another file specified in the settings file under DB_BACKUP_PATH.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> python manage.py runscript create_database_backup
"Backup created successfully: [FULL_PATH]\\mentorship-program\\mentorship_program_project\\DATABASE_BACKUPS\\mentorship_app_2024-04-09_23-20-06.sql.tar.sql"
"Media folder has been backedup in [FULL_PATH]\\mentorship-program\\mentorship_program_project\\DATABASE_BACKUPS\\media_2024-04-09_23-20-06.tar.gz"

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
from mentorship_program_project.settings import BACKUP_DATABASE_ROOT
from mentorship_program_project.settings import MEDIA_ROOT, BACKUP_DATABASE_ROOT, MEDIA_URL
from utils.database_backup import *

def run():
    postgresql_backup()
    media_backup()
    
    return 0


def postgresql_backup():
    """
    Description
    -----------
    Dumps the database to a place specified by DB_BACKUP_PATH in settings.py

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
    "Backup created successfully: [FULL_PATH]\\mentorship-program\\mentorship_program_project\DATABASE_BACKUPS\\mentorship_app_2024-04-09_23-20-06.sql"

    Authors
    -------
    Justin Goupil
    """
    DB_NAME = os.environ.get('DB_NAME')

 

    try:
        str_time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"{os.environ.get('DB_NAME')}_{str_time_stamp}.sql"
        backup_file_path = os.path.join(f"{BACKUP_DATABASE_ROOT}", f"{backup_file}")
        tarball_path = f"{backup_file_path}.tar.gz"

        if not os.path.exists(BACKUP_DATABASE_ROOT):
            raise FileNotFoundError(f"The directory does not exist: {BACKUP_DATABASE_ROOT}")

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

        #Remove the oldest file
        remove_oldest_file(DB_NAME, ".sql.tar.gz")


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
    
def media_backup():
    #print("Hello World :)")
    """
    Description
    -----------
    Creates a .tar.gz copy of the media folder and stores it under DB_BACKUP_PATH in the settings file.

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

    >>> python manage.py runscript create_media_backup
    "Media folder has been backedup in [FULL_PATH]\\mentorship-program\\mentorship_program_project\DATABASE_BACKUPS\\media_2024-04-09_23-20-06.tar.gz"


    Authors
    -------
    Justin Goupil
    """
    try:
        str_time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"media_{str_time_stamp}"
        backup_file_path = f"{BACKUP_DATABASE_ROOT}/{backup_file}"
        tarball_path = f"{backup_file_path}.tar.gz"

        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(os.path.join(f'{MEDIA_ROOT}', 'images'), arcname=os.path.basename(os.path.join(f'{MEDIA_ROOT}', 'images')))
        
        #Remove the oldest file
        remove_oldest_file("media",".tar.gz")

        print(f"Media folder has been backed up in {tarball_path}.")
        return 0
            
    except FileExistsError as e:
        #This should never happen, but just in case it does.
        print(f"This file already exists: {backup_file_path}\nError: {e}\n")
        return 1
    

