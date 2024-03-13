"""
FILE NAME: backend_requests.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

For view routes that are not necessarily visually displayed by the user, but none
the less change the database.

These would be things you do not navigate too, but generally would request the 
back end server perform, think post requests

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
import mentorship_program_app.view_routes.backend_requests
from django.urls import path

# in urls.py

...
path('request_mentor/<int:mentee_id>/<int:mentor_id>',
                    backend_requests.request_mentor,
                    name='request mentor'),
...
-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

"""

from utils import security
from mentorship_program_app.view_routes.status_codes import bad_request_400
from django.http import HttpResponse,HttpRequest
import json

from mentorship_program_app.models import *

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
    print('Hello')
    
    
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

    mentorship_request = MentorshipRequest.create_request(mentor_account.id,mentee_account.id)
    if mentorship_request: 
        mentorship_request.save() 
    else:
        print("this request already exists, IDENTITY CRISIS ERROR 🤿  ⛰️")

    ##print_debug(user.has_requested_user(mentor_id))
    return HttpResponse(json.dumps({"result":"created request!"}));

def cancel_request(req : HttpRequest,mentee_id : int,mentor_id : int)->HttpResponse:
    '''
     Description
     ___________
     view that removes a mentor request using the mentor and mentee id

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
        >>> cancel_request(request,mentee_id,mentor_id)

        /path/to/route/mentee_id/mentor_id

     >>> 
     Authors
     _______
     Andy Nguyen Do *^*
    '''
    user = User.from_session(req.session)
    
    
    #If you are a mentee you can only request for yourself
    if user.is_mentee():
        mentee_id : int = user.id
    elif user.is_mentor() and mentee_id == None:
        return bad_request_400("mentee id required for mentors")

    ##print_debug(user.has_requested_user(mentor_id))
    mentor_account = None
    mentee_account = None
    
    #If mentor account does not exists
    try:
        mentor_account = User.objects.get(id=mentor_id)
    except ObjectDoesNotExist:
        return bad_request_400("invalid mentor id detected!")
    
    #If mentor account does not exists
    try:
        mentee_account = User.objects.get(id=mentee_id)
    except ObjectDoesNotExist:
        return bad_request_400("invalid mentee id detected!")
    
    if mentor_account == None or mentee_account == None:
        #we should never get here, but just in case for some reason
        return bad_request_400("internal error occured")
    
    MentorshipRequest.remove_request(mentee_id, mentor_id)
    print("Request has been removed. Guess ya didn't like 'em huh :(")