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
from  mentorship_program_app.models import Users, Biographies
from datetime import date
import traceback

def createUser(strEmailAddress: str, strPasswordHash:str, objRole:Users.Role, 
               strFirstname:str, strLastName:str, strPhoneNumber:str, 
               clsDateOfBirth:date, strGender:str, strPreferredPronouns:str, strSessionID:str, strSessionKeyHash:str, strBio):
    try:
        Users.objects.create(
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
        user = Users.objects.get(clsEmailAddress = strEmailAddress)
        Biographies.objects.create(intUserID = user, strBio = strBio)
        return True
    except Exception as e:
        traceback.print_exc()
        return False
        
def getUserLogin(clsEmailAddress: str):
    """
    Returns a users password hash. Returns None if a User is not found or has no password hash. 
    """
    return Users.objects.filter(clsEmailAddress = clsEmailAddress).values('strPasswordHash')
    

def getUserID(strEmailAddress:str):
    """
    Returns a users ID. Returns None if a User is not found or account doesn't exist. 
    """
    return Users.objects.filter(clsEmailAddress = strEmailAddress).values('id')
    

def updatePassword(strEmailAddress: str, strNewHash: str):
    """
    Returns True if users password is successfully updated. 
    """
    try:
        user = Users.objects.get(clsEmailAddress=strEmailAddress)
        user.strPasswordHash = strNewHash
        user.save()
        return True
    except Exception as e:
        return False
    

def getUserInformation(intID:int):
    return Users.objects.get(id=intID) & Users.biography_set
     
     

    