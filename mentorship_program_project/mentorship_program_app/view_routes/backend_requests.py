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
from ..models import User
from datetime import date
from dateutil.relativedelta import relativedelta
import json
from ..views import invalid_request_401

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
    return HttpResponse(json.dumps({"result":"created request!"}))

@User.Decorators.require_logged_in_super_admin(invalid_request_401)
def verify_mentee_ug_status(req : HttpRequest) -> int:
    """
    Description
    -----------
    Sets any mentee that is not an undergrad student to inactive

    NOTE: This implementation is flawed, but the best solution requires getting
    information from IT, which isn't feasible.

    Parameters
    ----------
    - req (HttpRequest): Unused, but required for the decorator

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - int: The count of mentee accounts set as inactive

    Example Usage
    -------------

    >>> path('verify_mentees/', backend_requests.verify_mentee_ug_status,
            name='verify mentees')
    7

    Authors
    -------
    Andy Do
    William Lipscom:b
    """
    inactive_users = User.objects.filter((User.cls_date_joined + relativedelta(years=4) < date.today))
    int_inactive_count = 0
    for u in inactive_users:
        #u.bln_account_disabled = True
        u.bln_active = False
        u.cls_active_changed_date = date.today
        int_inactive_count += 1
    #print("Disabled all inactive users.")
    return int_inactive_count