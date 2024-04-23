"""
FILE NAME: restore_database_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script that restores a backup of the database to the postgresql 
database specified under DB_NAME in settings.py.
This script accepts .sql.tar.gz file type.
Input file must follow "[DATABASE NAME]_YEAR-MONTH-DAY_HOUR-MINUTE-SECOND.sql.tar.gz" format.

NOTE: THE DATABASE MUST BE EMPTY.
NOTE: Input file must follow "[DATABASE NAME]_YEAR-MONTH-DAY_HOUR-MINUTE-SECOND.sql.tar.gz" format.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> python manage.py runscript restore_database_backup
"-PRINTS OUT ALL ACTIONS TAKEN-"
"Database restored successfully."

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
import os
import tarfile
from mentorship_program_project.settings import BACKUP_DATABASE_ROOT

def run():
    """
    Description
    -----------
    Restores the database from a path specified by the user.
    Input file must follow "[DATABASE NAME]_YEAR-MONTH-DAY_HOUR-MINUTE-SECOND.sql.tar.gz" format.

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - None

    Example Usage
    -------------

    >>> python manage.py runscript restore_database_backup
    "Hello, please enter the direct path of the .sql.tar.gz file."
    "Tar file direct path: [FULL_PATH]\\mentorship-program\\mentorship_program_project\\DATABASE_BACKUPS\\media_2024-04-09_23-20-06.tar.gz"
    "-PRINTS OUT ALL ACTIONS TAKEN-"
    "Database restored successfully."

    Authors
    -------
    Justin Goupil
    """
    print("Hello, please enter the direct path of the .sql.tar.gz file.")
    tar_path = input("Tar file direct path: ").strip()

    if not os.path.exists(tar_path):
        print(f"Error: The File does not exist: {tar_path}")
        return 1
    
    try:
        sql_file = extract_sql_file(tar_path)

        restore_database(os.path.join(f'{BACKUP_DATABASE_ROOT}', f'{sql_file}'))

        print(f"\n\nThe database has been restored from {tar_path}\n")

        return 0
    except Exception as e:
        str_error_msg = f"Error: {e}"
        print(str_error_msg)
        return 1
    
    #print(sql_file)




def extract_sql_file(tar_path):
    """
    Returns sql_file
    """
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar.getmembers():
            if(member.name.endswith('.sql')):
                sql_file = member.name
                tar.extract(member, BACKUP_DATABASE_ROOT)
            else:
                raise FileNotFoundError("No SQL file was found.")
                
    return sql_file.strip()

def restore_database(sql_file):

    str_encoded_password = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD"))
    
    command = [
            'psql',
            '-f',
            f'{sql_file}',
            f'postgresql://{os.environ.get("DB_USER")}:{str_encoded_password}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
        ]
    
    try:

        subprocess.run(command, check=True)

        #Remove the uncompressed file
        os.remove(sql_file)

    except Exception as e:
        str_error_msg = f"Error encounterd: "
        print(str_error_msg)