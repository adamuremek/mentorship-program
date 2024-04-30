"""
/*********************************************************************/
/* FILE NAME: account_routes.py                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Adam U., Andrew P., Jordan A.                         */
/* (OFFICIAL) DATE CREATED: Long ago                                 */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for managing user accounts including  */
/* enabling, disabling, and deactivating accounts within the         */
/* Mentorship Program for SVSU CSIS students and mentors.            */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the backend logic for managing user accounts.  */
/* Functions include enabling, disabling, and deactivating user      */
/* accounts. This file is included in the server-side logic of       */
/* 'combined_views.html'.                                            */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: Class for handling HTTP requests                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for parsing JSON data                              */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*                                                                   */
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

import json
from django.http import HttpResponse, HttpRequest
from django.shortcuts import  redirect
from mentorship_program_app.models import *
from .emails import *
from ..models import *


def deactivate_your_own_account(req : HttpRequest):
    """
    Function to deactivate (inactivate) a user's own account. Sends notifications to associated mentors or mentees.

    Parameters:
    - req : HttpRequest : HTTP request object containing session data.

    Returns:
    - Redirect : redirects user to the logout URL after inactivation.
    """
    user = User.from_session(req.session)
    if(user.str_role == "Mentee"):
        if not user.mentee.mentor == None:
           mentor = User.objects.get(id=Mentor.objects.get(id=user.mentee.mentor_id).account_id)
           send_to = mentor.cls_email_address
           your_mentor_quit(send_to , "Mentee")
    else:
        mentees_for_mentor = user.mentor.mentee_set.all()
        for mentee in mentees_for_mentor:
            send_to = User.objects.get(id=mentee.account_id)
            email_address = send_to.cls_email_address
            your_mentor_quit(email_address, "Mentor")

    User.make_user_inactive(User.objects.get(id=User.from_session(req.session).id), "User inactivated their account")
    return redirect('/logout')

def enable_user(req:HttpRequest):
    '''
    Description
    -----------
    Function to enable a user by enabling their account.
    
    Parameters
    ----------
    - req : HttpRequest: HTTP request object containing a user who was enabled.
    
    Returns
    -------
    HttpResponse: HTTP response confirming the enable action.
    
    Example Usage
    -------------
    This function is typically called via an HTTP POST request with JSON data containing the user's ID and the confirmation of enable.
    
    >>> enable_user(req)
    "user {id} has been enabled"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    '''
    post_data = json.loads(req.body.decode("utf-8"))
        
    id = post_data["id"] if "id" in post_data else None

    # Validate user id 
    if(id == None):
        return HttpResponse("User doesn't exist")
    
    # Get the user and set their disabled field to False
    user = User.objects.get(id=id)
    user.bln_account_disabled = False
    user.bln_active = True    
    # Save changes to user object
    user.save()
    
    return HttpResponse(f"user {id}'s status has been changed to enabled")

def disable_user(req:HttpRequest):
    '''
    Description
    -----------
    Function to disable a user by disabling their account.
    
    Parameters
    ----------
    - req : HttpRequest: HTTP request object containing a user who was disabled.
    
    Returns
    -------
    HttpResponse: HTTP response confirming the disable action.
    
    Example Usage
    -------------
    This function is typically called via an HTTP POST request with JSON data containing the user's ID and the confirmation of disable.
    
    >>> disable_user(req)
    "user {id} has been disabled"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    '''

    post_data = json.loads(req.body.decode("utf-8"))
        
    id = post_data["id"] if "id" in post_data else None

    # Validate user id 
    if(id == None):
        return HttpResponse("User doesn't exist")
    
    # Get the user and set their disabled field to True
    user = User.objects.get(id=id)

    if not user.is_super_admin:
        return

    User.disable_user(user, "User was deactivated")
    
    if(user.str_role == "Mentee"):
        mentee_account = Mentee.objects.get(account_id=user.id)
        if not mentee_account.mentor == None:
           mentor = User.objects.get(id=Mentor.objects.get(id=user.account.mentor).account_id)
           send_to = mentor.cls_email_address
           your_mentor_quit(send_to , "Mentee")
    else:
        mentees_for_mentor = user.mentor.mentee_set.all()
        for mentee in mentees_for_mentor:
            send_to = User.objects.get(id=mentee.account_id)
            email_address = send_to.cls_email_address
            your_mentor_quit(email_address, "Mentor")


    response = HttpResponse(f"user {id}'s status has been changed to disabled")
    response.status_code = 200
    return response