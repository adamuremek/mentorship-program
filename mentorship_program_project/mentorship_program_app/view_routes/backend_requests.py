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
from django.shortcuts import redirect
from ..models import User
from datetime import date
from dateutil import relativedelta
import json
from ..models import SystemLogs
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

#@User.Decorators.require_logged_in_super_admin(invalid_request_401)
def verify_mentee_ug_status(req : HttpRequest) -> HttpResponse:
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
    - HttpResponse: The http reponse for the redirect

    Example Usage
    -------------

    >>> path('verify_mentees/', backend_requests.verify_mentee_ug_status,
            name='verify mentees')
    7

    Authors
    -------
    Andy Do
    William Lipscom:b
    Jordan Anodjo
    """

    inactive_mentees = User.objects.filter(cls_date_joined__lte=date.today() - relativedelta(years=4), str_role="Mentee", bln_account_disabled=False, bln_active=True)

    for mentee in inactive_mentees:
        #Set inactive
        mentee.bln_active = False
        mentee.cls_active_changed_date = date.today()
        mentee.save()
        # record logs
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTEE_DEACTIVATED, specified_user=mentee)

    return redirect('/admin_dashboard')

@security.Decorators.require_login(bad_request_400)
def create_new_interest(req : HttpRequest, admin_id : int, str_interest : str, bool_is_default : bool)->HttpResponse:
    '''
     Description
     ___________
     view that creates a mentor request between a given mentor id 
     and mentee id

     Paramaters
     __________
        req : HttpRequest - django http request
        admin_id : int - admin id from the datbase, must be valid.
        str_interest : str - The name of an interest.
        bool_is_default : bool - Used to set it interest is a default option or not.

     Returns
     _______
        HttpResponse containing a 400 response for invalid information or a response for valid information.
     
     Example Usage
     _____________
        >>> create_new_interest(/create_interest, 12, "Computer Science", True)

 
     Authors
     _______
     Justin Goupil
    '''
        
    admin = User.from_session(req.session)
    bool_error = False
    str_error_message = "The following error(s) occured: \n"
    new_interest : 'Interest' = None

    #Check if the user is an admin.
    if admin.Role != User.Role.ADMIN :
        str_error_message.join("Not an administrator. \n")
        bool_error = True
        
    #Check if the str_interest is empty.
    if len(str_interest) == 0 :
        str_error_message.join("Interest cannot be empty. \n")
        bool_error = True
    #Check if the str_interest exists.
    elif  Interest.get_interest(str_interest) == None :
        str_error_message.join("Interest already exists. \n")
        bool_error = True

    #Create the interest.
    if not(bool_error) : 
        new_interest = Interest.create_interest(str_interest, bool_is_default)
        
    #Check if the interest was created.
    if new_interest == None or bool_error:
        str_error_message.join("Interest creation failed. \n")
        bool_error = True

    if bool_error :
        bad_request_400(str_error_message)
    else:
        #All is good.
        return HttpRequest("Interest Added.")
    

@security.Decorators.require_login(bad_request_400)
def resolve_report(req: HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Resolves a report by setting the bln_resolved field to True

    Parameters
    ----------
    - req (HttpRequest): The request object

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The http response for the redirect

    Example Usage
    -------------
    >>> path('resolve_report/', backend_requests.resolve_report, name='resolve report')

    Authors
    -------
    Quinn F. 
    """

    user = User.from_session(req.session)
    str_error_message = "The following error(s) occured:"
    errors =  []
    errors.append(str_error_message)
    bool_error = False

    if not user.is_super_admin() :
        errors.append("Not an administrator.")
        bool_error = True

    report_id = req.POST['report_id']
    if report_id == None:
        errors.append("Report ID is required.")
        bool_error = True
    
    try:
        UserReport.get_report_id(report_id)
    except ObjectDoesNotExist:
        errors.append("Invalid report ID.")
        bool_error = True

    if bool_error :
        return bad_request_400("\n".join(errors))
    else:
        report_id = req.POST['report_id']
        UserReport.resolve_report(report_id)
        return redirect('/admin_reported_users')

@security.Decorators.require_login(bad_request_400)
def report_user(req: HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Creates a new user report

    Parameters
    ----------
    - req (HttpRequest): The request object

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The http response for the redirect

    Example Usage
    -------------
    >>> path('report_user/', backend_requests.report_user, name='report user')

    Authors
    -------
    Quinn F. 
    """

    user = User.from_session(req.session)
    str_error_message = "The following error(s) occured:"
    errors =  []
    errors.append(str_error_message)
    bool_error = False

    try:
        User.objects.get(id=req.POST.get("reported_user_id", None))
    except ObjectDoesNotExist:
        errors.append("Invalid reported user ID.")
        bool_error = True

    if not req.POST.get("report_type", None):
        errors.append("Report type is required.")
        bool_error = True
    
    if not req.POST.get("report_reason", None):
        errors.append("Report reason is required.")
        bool_error = True    
    
    if bool_error:
        return bad_request_400("\n".join(errors))
    else:
        reported_user_id = req.POST['reported_user_id']
        report_type = req.POST['report_type']
        report_reason = req.POST['report_reason']
        UserReport.create_user_report(report_type, report_reason, reported_user_id)
        return redirect('/universal_profile/' + reported_user_id)
