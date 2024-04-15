"""
/*********************************************************************/
/* FILE NAME: request_session_user_data_rout.py                      */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: David K (I think)                                     */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to enhance user interactivity by providing      */
/* real-time data fetching capabilities, significantly improving the */
/* responsiveness and dynamism of the user interface on the          */
/* mentorship platform.                                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file handles the dynamic retrieval of session user data      */
/* based on HTTP requests, enabling AJAX-driven updates without      */
/* page reloads. It serves as a backend utility for front-end        */
/* forms and applications to fetch user-specific data dynamically.   */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for JSON encoding                                  */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
import json
from django.http import HttpResponse, HttpRequest
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from .emails import *
from ..models import *

@security.Decorators.require_login(bad_request_400)
def request_session_user_data(req : HttpRequest):
    '''
    Description
    ___________
    convinence view that gets requested data from the current session user and returns it as a dictionary
    this is so that front end forms can update over ajax from the given user data

    Usage
    ------
    <route>/request_session_user_data?data=str_first_name,str_last_name
    >>> returns
    {str_first_name:<firstname>,str_last_name:<lastname>}

    '''
    session_user : User = User.from_session(req.session)
    print(session_user)
    session_user = session_user.sanitize_black_properties() #ensure only safe data gets sent to front end

    if req.GET:

        ret_val = {}
        if "data" in req.GET:
            data = req.GET["data"].split(",")

            for key in data:
                ret_val[key] = session_user.__dict__[key]

        if "request" in req.GET:
            requests = req.GET["request"].split(",")

            for query_req in requests:
                if query_req not in ret_val:
                        if query_req == "has_maxed_mentee_requests":
                            ret_val["has_maxed_mentee_requests"] = session_user.is_mentee() and \
                                    session_user.mentee.has_maxed_request_count()

        return HttpResponse(json.dumps(ret_val))
    
    return bad_request_400("get data required")