from models import *
from datetime import date

def createUser(strEmailAddress: str, strPasswordHash:str, objRole:Users.Role, clsDateJoined:date, clsActiveChangedDate:date, 
               blnActive:bool, blnAccountDisabled:bool, strFirstname:str, strLastName:str, strPhoneNumber:str, 
               clsDateOfBirth:date, strGender:str, strPreferredPronouns:str, strSessionID:str, strSessionKeyHash:str):
    
    user = Users()
    user.clsEmailAddress = strEmailAddress
    user.strPasswordHash = strPasswordHash
    user.strRole = objRole
    user.clsDateJoined = clsDateJoined
    user.clsActiveChangedDate = clsActiveChangedDate
    user.blnActive = blnActive
    user.blnAccountDisabled = blnAccountDisabled
    user.strFirstName = strFirstname
    user.strLastName = strLastName
    user.strPhoneNumber = strPhoneNumber
    user.clsDateofBirth = clsDateOfBirth
    user.strGender = strGender
    user.strPreferredPronouns = strPreferredPronouns
    user.strSessionID = strSessionID
    user.strSessionKeyHash = strSessionKeyHash
    
    user.save()
    
def getUserLogin(strEmail: str, strPasswordHash: str):
    """
    Returns a users 
    """
    return  Users.objects.filter(clsEmailAddress = strEmail).values('strPasswordHash')
    

def getUserID(intID: int):
    """
    
    """

    clsUser = Users.objects.filter(id = intID)

    
    