"""
FILE NAME: create_media_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script that creates a .tar.gz copy of the media folder and stores it under 
DB_BACKUP_PATH in the env file.


-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> python manage.py runscript create_media_backup

    
    "Backup created successfully: [FULL_PATH]\mentorship-program\mentorship_program_project\DATABASE_BACKUPS\media_2024-04-09_23-20-06.tar.gz"
    

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT

"""

from datetime import datetime
import os
import tarfile
from mentorship_program_project.settings import MEDIA_ROOT, BACKUP_DATABASE_ROOT, MEDIA_URL
from utils.database_backup import *

def run():
    #print("Hello World :)")
    """
    Description
    -----------
    Creates a .tar.gz copy of the media folder and stores it under DB_BACKUP_PATH in the env file.

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
    "Media folder has been backedup in [FULL_PATH]\mentorship-program\mentorship_program_project\DATABASE_BACKUPS\media_2024-04-09_23-20-06.tar.gz"


    Authors
    -------
    Justin Goupil
    """
    try:
        print (MEDIA_URL)
        str_time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f"media_{str_time_stamp}"
        backup_file_path = f"{BACKUP_DATABASE_ROOT}/{backup_file}"
        tarball_path = f"{backup_file_path}.tar.gz"

        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(f'{MEDIA_ROOT}\\images', arcname=os.path.basename(f'{MEDIA_ROOT}\\images'))
        
        #Remove the oldest file
        remove_oldest_file("media",".tar.gz")

        print(f"Media folder has been backed up in {tarball_path}.")
        return 0
            
    except FileExistsError as e:
        #This should never happen, but just in case it does.
        print(f"This file already exists: {backup_file_path}\nError: {e}\n")
        return 1
    

