"""
/*********************************************************************/
/* FILE NAME: mentorship_routes.py                                   */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: David K. and Others                                   */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate secure and efficient management   */
/* of various functionalities within the mentorship platform. The    */
/* specific responsibilities of this file could include handling     */
/* specific data processes, interactions, or other unique functions  */
/* within the platform that have not been detailed in this generic   */
/* header.                                                           */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* The specific purpose of this file should be described here. If    */
/* the file handles multiple distinct functionalities, a brief       */
/* description of each is helpful.                                   */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* Depending on what this file does, list the Django imports used.   */
/* For example, if it handles database interactions:                 */
/* - models: For accessing the database models                       */
/* - transaction: For managing database transactions                 */
/* Or, for handling HTTP requests:                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - HttpRequest: For obtaining details of HTTP requests             */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */

/*********************************************************************/
"""

import json
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import  redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from .emails import *
from ..models import *

from typing import Dict
@security.Decorators.require_login(bad_request_400)
def create_mentorship(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    """
    Description
    ___________
    creates a mentorship relation between the given mentor and mentee ids

    Authors
    _______
    David Kennamer .._..
    """
    session_user = User.from_session(req.session)

    session_user.create_mentorship_from_user_ids(mentee_user_account_id, mentor_user_account_id)

    return HttpResponse("created request sucessfully")

@security.Decorators.require_login(bad_request_400)
def delete_mentorship(req: HttpRequest, mentee_user_account_id : int):
    '''
    Description
    -----------
    Function to dissociate a mentee from their current mentor based on the mentee's account ID. 
    It sets the `mentor_id` of the specified Mentee object to None, thereby removing the mentor-mentee relationship.
    After the operation, it redirects the user to the previous page.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing all details of the request.
    - mentee_user_account_id : int
        The account ID of the mentee whose mentorship is to be deleted.

    Returns
    -------
    HttpResponseRedirect
        Redirects the user to the page they came from, as indicated by the HTTP_REFERER header, 
        or to the homepage if the referrer is not available.

    Example Usage
    -------------
    Assuming a mentee with an account ID of 123 exists and is currently associated with a mentor:

        >>> from django.http import HttpRequest
        >>> request = HttpRequest()
        >>> delete_mentorship(request, 123)

        This will remove the mentee's current mentor association and redirect the user to the referring page.

    Authors
    -------
    - Andrew P
    - Anthony P. (small fix checking id to checking account for mentee object)
'''
    mentee = Mentee.objects.get(account_id=mentee_user_account_id)
    mentee.mentor_id = None
    mentee.save()

    mentee_account = None

    try:
        mentee_account = User.objects.get(id=mentee_user_account_id)
    except ObjectDoesNotExist:
        return bad_request_400("invalid id detected!")
    

    email_for_mentor_removed_you(mentee_account.cls_email_address)

    session_user = User.from_session(req.session)
    SystemLogs.objects.create(str_event=SystemLogs.Event.MENTORSHIP_TERMINATED_EVENT, specified_user=session_user)

    # redirect to the page the request came from
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))


@security.Decorators.require_login(bad_request_400)
def accept_mentorship_request(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    session_user = User.from_session(req.session)
    mentor_account = None
    mentee_account = None
    try:
        mentor_account = User.objects.get(id=mentor_user_account_id)
        mentee_account = User.objects.get(id=mentee_user_account_id)
    except ObjectDoesNotExist:
        return bad_request_400("mentor id is invalid!")

    if not mentor_account.bln_active or not mentee_account.bln_active:
        return bad_request_400("User is no longer active")
    
    if session_user.is_super_admin() or session_user.id == mentee_user_account_id or session_user.id == mentor_user_account_id:
        try:
            mentorship_request = MentorshipRequest.objects.get(
                                        mentor_id=mentor_user_account_id,
                                        mentee_id=mentee_user_account_id
                                        )
            
        
            #we should never get here, but just in case
            #we should never get here, but just in case
            # if mentorship_request.is_accepted():
            #     return bad_request_400("you already accepted this request!")

            sucessful = None
            try:
                sucessful = mentorship_request.accept_request(session_user)
                email_for_mentorship_acceptance(mentor_account.cls_email_address, mentee_account.cls_email_address)
                mentor = Mentor.objects.get(account_id=mentor_account.id)
                number_of_mentees_this_mentor_has= mentor.mentee_set.all()
                max_number_of_mentees = mentor.int_max_mentees

                if number_of_mentees_this_mentor_has == max_number_of_mentees:
                    delete_these_requests = MentorshipRequest.objects.get(mentor_id=mentee_account.id)
                    for request in delete_these_requests:
                        user_to_send_to = User.objects.get(id=request.requester)
                        email_for_mentorship_rejection(user_to_send_to)
                    delete_these_requests.delete()
                        
                    
            except ValidationError:
                #this mentor has max mentees
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            
            if sucessful:
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            
            return bad_request_400("unable to create request!")

        except ObjectDoesNotExist:
            return bad_request_400("you do not have a request to accept!")
    return bad_request_400("permission denied!")

@security.Decorators.require_login(bad_request_400)
def request_mentor(req : HttpRequest,mentee_id : int,mentor_id : int)->HttpResponse:
    '''
     Description
     ___________
     view that creates a mentor request between a given mentor id 
     and mentee id

     Paramaters
     __________
        req : HttpRequest - django http request
        mentee_id : int - mentee id from the datbase, must be valid
        mentor_id : int - mentee id from the database, must be valid

     Returns
     _______
        HttpResponse containing a valid json ok signature or 401 error code for invalid data
     
     Example Usage
     _____________
        >>> request_mentor(request,mentee_id,mentor_id)

        /path/to/route/mentee_id/mentor_id

     >>> 
     Authors
     _______
     David Kennamer *^*
    '''
    user = User.from_session(req.session)
    #if you are a mentee you can only request for yourself
    if user.is_mentee():
        mentee_id : int = user.id
    elif user.is_mentor() and mentee_id == None:
        return bad_request_400("mentee id required for mentors")

    ##print_debug(user.has_requested_user(mentor_id))
    mentor_account = None
    mentee_account = None
    
    try:
        mentor_account = User.objects.get(id=mentor_id)
        mentee_account = User.objects.get(id=mentee_id)
    except ObjectDoesNotExist:
        return bad_request_400("invalid id detected!")
    
    if mentor_account == None or mentee_account == None:
        #we should never get here, but just in case for some reason
        return bad_request_400("internal error occured")

    if user.id == mentor_account.id:
        you_have_a_new_request(mentee_account.cls_email_address)
    else:
        if not Mentee.objects.get(account_id=user.id).mentor:
            you_have_a_new_request(mentor_account.cls_email_address)

    # check to make sure a mentorship doesn't already exist
    mentor_account_mentor = Mentor.objects.get(account_id=mentor_account.id)
    mentees = Mentee.objects.all().filter(mentor=mentor_account_mentor)

    for mentee in mentees: 
        if mentee_id == mentee.account_id:
            return bad_request_400("mentee already in mentorship with this mentor")


    mentorship_request = MentorshipRequest.create_request(mentor_account.id,mentee_account.id, user.id)
    if type(mentorship_request) == int:
        #there was an error creating the request
        response = HttpResponse(
                json.dumps(
                    {
                        "result":MentorshipRequest.ErrorCode.error_code_to_string(
                                                                mentorship_request
                                                                )
                    }
                    )
                )

        response.status_code = 400
        return response
    else: 
        mentorship_request.save()
    ##print_debug(user.has_requested_user(mentor_id))
    return HttpResponse(
            json.dumps(
                    {
                        "result":"created request!",
                        "has_maxed_mentee_requests": user.is_mentee() and user.mentee.has_maxed_request_count()
                    }
                )
            )

@security.Decorators.require_login(bad_request_400)
def reject_mentorship_request(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    session_user = User.from_session(req.session)
    mentor_account = None
    try:
        mentor_account = User.objects.get(id=mentor_user_account_id)
    except ObjectDoesNotExist:
        return bad_request_400("mentor id is invalid!")

    if session_user.is_super_admin() or session_user.id == mentee_user_account_id or session_user.id == mentor_user_account_id:
        try:
            mentorship_request = MentorshipRequest.objects.get(
                                        mentor_id=mentor_user_account_id,
                                        mentee_id=mentee_user_account_id
                                        )
            try:
                # send a declined email to whoever requested the mentorship
                send_to = User.objects.get(id=mentorship_request.requester)
                # if you cancel your own request, don't get an email for it
                if not session_user.id == send_to.id:
                    email_for_mentorship_rejection(send_to.cls_email_address)


                mentorship_request.delete()
                
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            except:
                return bad_request_400("unable to create request!")

        except ObjectDoesNotExist:
            return bad_request_400("you do not have a request to accept!")
    return bad_request_400("permission denied!")