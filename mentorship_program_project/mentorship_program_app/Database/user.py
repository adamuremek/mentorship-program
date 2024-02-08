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
        
def getUserLogin(strEmail: str):
    """
    Returns a users password hash. Returns None if a User is not found or has no password hash. 
    """
    return Users.objects.filter(clsEmailAddress = strEmail).values('strPasswordHash')
    

def updateUser(strFirstName:str, strLastName:str, str):
    user = Users()
     
    