"""
FILE NAME: user.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED: February 08, 2024

-------------------------------------------------------------------------------
FILE PURPOSE:
Handles the CRUD operations pertaining to the User model in the database.

-------------------------------------------------------------------------------
COMMAND LINE PARAMETER LIST (In Parameter Order):
(NONE)

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
from mentorship_program_app.Database import user
clsExUser = user

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT
WJL  2/19/24   Added and updated comments across the entire file
"""

from  mentorship_program_app.models import *
from datetime import date
import traceback
import json

def createUser(strEmailAddress: str, strPasswordHash:str, objRole:User.Role, 
               strFirstname:str, strLastName:str, strPhoneNumber:str, 
               clsDateOfBirth:date, strGender:str, strPreferredPronouns:str, strSessionID:str, strSessionKeyHash:str, strBio):
    try:
        User.objects.create(
        clsEmailAddress = strEmailAddress,
        strPasswordHash = strPasswordHash,
        strRole = objRole,
        clsDateJoined = date.today(),
        clsActiveChangedDate = date.today(),
        blnActive = True,
        blnAccountDisabled = False,
        strFirstName = strFirstname,
        strLastName = strLastName,
        strPhoneNumber = strPhoneNumber,
        clsDateofBirth = clsDateOfBirth,
        strGender = strGender,
        strPreferredPronouns = strPreferredPronouns,
        strSessionID = strSessionID,
        strSessionKeyHash = strSessionKeyHash
        )
        user = User.objects.get(clsEmailAddress = strEmailAddress)
        Biographies.objects.create(intUserID = user, strBio = strBio)
        return True
    except Exception as e:
        traceback.print_exc()
        return False
        
def getUserLogin(clsEmailAddress: str):
    """
    Description
    -----------
    Retrieves a password hash associated with a given user's email

    Parameters
    ----------
    - clsEmailAddress (str): The user's email address

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - str: The string of the password hash
    - None: The given email has no password associated with it

    Example Usage
    -------------

    >>> getUserLogin('fake@email.com')
    'adlkfy8o90q23gb876df'

    Authors
    -------
    
    """

    return User.objects.filter(clsEmailAddress = clsEmailAddress).values('strPasswordHash')
    

def getUserID(strEmailAddress:str):
    """
    Description
    -----------
    Retrieves a user ID associated with a given user's email

    Parameters
    ----------
    - strEmailAddress (str): The user's email address

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - int: The string of the password hash
    - None: The given email has no ID associated with it

    Example Usage
    -------------

    >>> getUserID('fake@email.com')
    157

    Authors
    -------
    
    """

    return User.objects.filter(clsEmailAddress = strEmailAddress).values('id')
    

def updatePassword(strEmailAddress: str, strNewHash: str):
    """
    Description
    -----------
    Update the password associate with a given user's email

    Parameters
    ----------
    - strEmailAddress (str): The user's email address
    - strNewHash (str): The hash of the new password

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - bool: The success flag of the operation

    Example Usage
    -------------

    >>> updatePassword('fake@email.com', '807hags92gKhbkfa')
    true

    Authors
    -------
    
    """

    try:
        user = User.objects.get(clsEmailAddress=strEmailAddress)
        user.strPasswordHash = strNewHash
        user.save()
        return True
    except Exception as e:
        return False
    
def getUserObject(intID:int):
    """
    Description
    -----------
    Retrieves a user object from the database by their ID

    Parameters
    ----------
    - intID (int): The desired user's ID

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - User: The request user object

    Example Usage
    -------------

    >>> getUserObject(157)
    <__main__.User object at 0x123456789>

    Authors
    -------
    
    """

    return User.objects.get(id=intID)
    
def addInterests(strNewInterest: str):
    """
    Description
    -----------
    Add a new interest to the database

    Parameters
    ----------
    - strInterest (str): The new interest

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    (None)

    Example Usage
    -------------

    >>> addInterests('Java')

    Authors
    -------
    
    """

    Interest.objects.create(strInterest=strNewInterest)
    
def getInterest(intInterest:int):
    """
    Description
    -----------
    Retrieves an interest object based on the interest ID

    Parameters
    ----------
    - intInterest (int): The desired interest's ID

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - Interest: The request interest object

    Example Usage
    -------------

    >>> getInterest(157)
    <__main__.Interest object at 0x987654321>

    Authors
    -------
    
    """

    return Interest.objects.get(id=intInterest)

def getAllInterests():
    """
    Description
    -----------
    Generates a JSON of all current interest

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - str: The JSON string of interests

    Example Usage
    -------------

    >>> getAllInterests()
    '{[c++, python, html, javascript, webdev, godot, calculus, AI]}'

    Authors
    -------
    
    """

    interests = Interest.objects.all()
    interests_json = [
    {"id": interest.id, "Interest": interest.strInterest}
    for interest in interests
    ]
    return json.dumps(interests_json)
    
#def addUserInterests(intUserID: int, intInterestID: int):
    """
    Description
    -----------
    Adds an interest (by ID) to a user (by ID)

    Parameters
    ----------
    - intUserID (int): The ID of the user to add the interest to
    - intInterestID (int): The ID of the interest to be added

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    (None)

    Example Usage
    -------------

    >>> addUserInterests(157, 39)

    Authors
    -------
    
    """

    #Create a new User_Interests object with the provided user and interest IDs
    #new_user_interest = user_interests(intUserID_id=intUserID, intInterestID_id=intInterestID)
    #Save the new User_Interests object to the database
    #new_user_interest.save()

    

def getUserInformation(intUserID: int):
    """
    Description
    -----------
    Retrieves all stored user info based on a user ID

    Parameters
    ----------
    - intUserID (int): The ID of the user whose info is being retrieved

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - dict: A dictionary of the user info
    - None: No user by that ID exists

    Example Usage
    -------------

    >>> getUserInformation(157)
    {'EmailAddress': 'fake@email.com, 'Role': 'Mentee',
    'DateJoined': '2/19/2024', 'ActiveChangedDate': '2/19/2024',
    'Active': true, 'AccountDisabled': false, 'FirstName': 'John',
    'LastName': 'Doe', 'PhoneNumber': '(123) 456-7890',
    'DateOfBirth': '1/23/2003', 'PrefferedPronouns': 'He/Him', 'interests':
    [python, webdev]}

    Authors
    -------
    
    """

    try:
        # Fetch the user with the specified ID and related biographies
        user = User.objects.select_related('biographies').get(pk=intUserID)
        
        # Fetch interests associated with the user
        #user_interests = User_Interests.objects.filter(intInterestID_id=intUserID)
        #interests = [interest.intUserID.strInterest for interest in user_interests]

        # Construct a dictionary containing user information and interests
        user_info = {
            "EmailAddress": user.clsEmailAddress,
            "Role": user.strRole,
            "DateJoined": user.clsDateJoined,
            "ActiveChangedDate": user.clsActiveChangedDate,
            "Active": user.blnActive,
            "AccountDisabled": user.blnAccountDisabled,
            "FirstName": user.strFirstName,
            "LastName": user.strLastName,
            "PhoneNumber": user.strPhoneNumber,
            "DateOfBirth": user.clsDateofBirth,
            "Gender": user.strGender,
            "PreferredPronouns": user.strPreferredPronouns,
            #"Interests": interests
        }

        return user_info
    except User.DoesNotExist:
        return None  # Or handle the case where user does not exist