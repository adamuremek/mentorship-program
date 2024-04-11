"""
FILE NAME: restore_media_backup.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script that restores the media directory from a .tar.gz.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

>>> python manage.py runscript restore_media_backup

    Hello, please enter the direct path of the .tar.gz file.
    Tar file direct path: C:\Users\User\backups\media_2024-04-10_17-48-18.tar.gz
    Media folder has been restored from C:\Users\User\backups\media_2024-04-10_17-48-18.tar.gz

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT

"""

import os
import tarfile

def run():
    #print("Hello World :)")
    """
    Description
    -----------
    Restores the media directory from a backup.

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

    >>> python manage.py runscript restore_media_backup
    prompt: Hello, please enter the direct path of the .tar.gz file.
    Tar file direct path: C:\Users\User\backups\media_2024-04-10_17-48-18.tar.gz
    Media folder has been restored from C:\Users\User\backups\media_2024-04-10_17-48-18.tar.gz

    Authors
    -------
    Justin Goupil
    """

    print("Hello, please enter the direct path of the .tar.gz file.")
    tar_path = input("Tar file direct path: ")

    if not os.path.exists(tar_path):
        print(f"Error: The File does not exist: {tar_path}")
        return 1
    
    extract_file(tar_path)
    print(f"Media folder has been restored from {tar_path}.")
    return 0
    



def extract_file(tar_path):
    """
    Returns file
    """
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar.getmembers():            
            file = member.name
            tar.extract(member, os.environ.get("MEDIA_ROOT"))
                      
    return file