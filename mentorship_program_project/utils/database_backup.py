"""
FILE NAME: database_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

Utility methods shared between the create media and database backup script files.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> Not a standalone file.

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT

"""

from mentorship_program_project.settings import BACKUP_DATABASE_ROOT, BACKUP_DATABASE_COUNT
import os
from datetime import datetime

def remove_oldest_file(str_file_name, str_file_extension):
    """
    Description
    -----------
    Given the prefix of a file and the extension discover the oldest file.

    Parameters
    ----------
    str_file_name (str): prefix of a file.
    str_file_extension (str): file extension.

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - None

    Example Usage
    -------------

    >>> remove_oldest_file("mentorship_app",".sql.tar.gz")
    None

    Authors
    -------
    Justin Goupil
    """

    if return_file_count(str_file_name) > BACKUP_DATABASE_COUNT:
        oldest_file_name =  return_oldest_file(str_file_name, str_file_extension)       
        os.remove(f"{BACKUP_DATABASE_ROOT}/{oldest_file_name}")
        return None
    else:
        return None    

def return_file_count(str_file_name):
    """
    Description
    -----------
    Checks the number of active backups currently stored in DATABASE_BACKUPS 

    Parameters
    ----------
    str_file_name (str): prefix of a file.

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - The number of files that start with str_file_name.

    Example Usage
    -------------

    >>> return_file_count("mentorship_app")
    4

    Authors
    -------
    Justin Goupil
    """

    int_count = 0
    for file_name in os.listdir(BACKUP_DATABASE_ROOT):
        if file_name.startswith(str_file_name):
            int_count += 1
    
    return int_count

def return_oldest_file(str_file_name, str_file_extension):
    """
    Description
    -----------
    Checks the number of active backups currently stored in DATABASE_BACKUPS 

    Parameters
    ----------
    str_file_name (str): prefix of a file.

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - str_oldest_file_name : the oldest file.

    Example Usage
    -------------

    >>> return_oldest_file("mentorship_app",".sql.tar.gz")
    mentorship_app_2024-04-11_17-05-52.sql.tar.gz

    Authors
    -------
    Justin Goupil
    """
    """
    Finds the oldest file in DATABASE_BACKUPS 

    Returns
    =======
    The number of files that start with str_file_name.
    """

    file_list = []
    oldest_file_time = datetime.now()
    str_oldest_file_name = None

    for file_name in os.listdir(BACKUP_DATABASE_ROOT):
        if file_name.startswith(str_file_name):
           file_list.insert(0, file_name)
    
    

    for file_name in file_list:

        str_file_date = ((file_name.removeprefix(str_file_name+'_')).removesuffix(str_file_extension)).replace("_","-")
        
        date_list = str_file_date.split("-")


        file_date = datetime(
            year=int(date_list[0]), 
            month=int(date_list[1]), 
            day=int(date_list[2]),
            hour=int(date_list[3]), 
            minute=int(date_list[4]), 
            second=int(date_list[5]))
        
        if oldest_file_time > file_date:
            oldest_file_time = file_date
            str_oldest_file_name = file_name

    return str_oldest_file_name