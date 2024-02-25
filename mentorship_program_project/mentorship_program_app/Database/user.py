"""
/*********************************************************************/
/*                   FILE NAME:  user.py                             */
/*********************************************************************/
/*                 PART OF PROJECT: Database				         */
/*********************************************************************/
/*                   WRITTEN BY:                                     */
/*		         DATE CREATED: February 08, 2024                     */
/*********************************************************************/
/*  PROJECT PURPOSE:								                 */
/*											                         */
/*                                                                   */
/*********************************************************************/
/*  FILE PURPOSE:                                                    */
/*											                         */
/*                                                                   */
/*********************************************************************/
/*  COMMAND LINE PARAMETER LIST (In Parameter Order):                */
/*  (NONE)                                                           */
/*********************************************************************/
/*  ENVIRONMENTAL RETURNS:							                 */
/*  (NOTHING)                                                        */
/*********************************************************************/
/* SAMPLE INVOCATION:                                                */
/*  from mentorship_program_app.Database import user				 */
/*  clsExUser = user										         */
/*********************************************************************/
/*  GLOBAL VARIABLE LIST (Alphabetically):                           */
/*	(NONE)					  	                                     */
/*********************************************************************/
/* COMPILATION NOTES:								                 */
/* 											                         */	
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*											                         */
/*  WHO   WHEN     WHAT                                              */
/*  ---   ----     ------------------------------------------------- */
/*********************************************************************/
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
    Returns a users password hash. Returns None if a User is not found or has no password hash. 
    """
    return User.objects.filter(clsEmailAddress = clsEmailAddress).values('strPasswordHash')
    

def getUserID(strEmailAddress:str):
    """
    Returns a users ID. Returns None if a User is not found or account doesn't exist. 
    """
    return User.objects.filter(clsEmailAddress = strEmailAddress).values('id')
    

def updatePassword(strEmailAddress: str, strNewHash: str):
    """
    Returns True if users password is successfully updated. 
    """
    try:
        user = User.objects.get(clsEmailAddress=strEmailAddress)
        user.strPasswordHash = strNewHash
        user.save()
        return True
    except Exception as e:
        return False
    
def getUserObject(intID:int):
    return User.objects.get(id=intID)
    
def addInterests(strNewInterest: str):
    Interest.objects.create(strInterest=strNewInterest)
    
def getInterest(intInterest:int):
    return Interest.objects.get(id=intInterest)

def getAllInterests():
        interests = Interest.objects.all()
        interests_json = [
        {"id": interest.id, "Interest": interest.strInterest}
        for interest in interests
    ]
        return json.dumps(interests_json)
    
#def addUserInterests(intUserID: int, intInterestID: int):
    #Create a new User_Interests object with the provided user and interest IDs
    #new_user_interest = user_interests(intUserID_id=intUserID, intInterestID_id=intInterestID)
    #Save the new User_Interests object to the database
    #new_user_interest.save()

    

def getUserInformation(intUserID: int):
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

     
     

    