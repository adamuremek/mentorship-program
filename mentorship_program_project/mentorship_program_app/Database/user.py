from models import *
from datetime import date
import traceback

def createUser(strEmailAddress: str, strPasswordHash:str, objRole:Users.Role, clsDateJoined:date, clsActiveChangedDate:date, 
               blnActive:bool, blnAccountDisabled:bool, strFirstname:str, strLastName:str, strPhoneNumber:str, 
               clsDateOfBirth:date, strGender:str, strPreferredPronouns:str, strSessionID:str, strSessionKeyHash:str):
    try:
        Users.objects.create(
        clsEmailAddress = strEmailAddress,
        strPasswordHash = strPasswordHash,
        strRole = objRole,
        clsDateJoined = clsDateJoined,
        clsActiveChangedDate = clsActiveChangedDate,
        blnActive = blnActive,
        blnAccountDisabled = blnAccountDisabled,
        strFirstName = strFirstname,
        strLastName = strLastName,
        strPhoneNumber = strPhoneNumber,
        clsDateofBirth = clsDateOfBirth,
        strGender = strGender,
        strPreferredPronouns = strPreferredPronouns,
        strSessionID = strSessionID,
        strSessionKeyHash = strSessionKeyHash
        )
        return True
    except Exception as e:
        traceback.print_exc()
        return False
        

    

def updateUser(strFirstName:str, strLastName:str, str):
    user = Users()
     
    