"""
/*********************************************************************/
/* FILE NAME: status_codes.py                                        */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: David K.                                              */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to standardize the handling of HTTP error       */
/* responses across the mentorship platform. This file defines      */
/* common error responses that can be reused in various parts of the */
/* application, enhancing maintainability and consistency.           */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains utility functions that return custom           */
/* HTTP error responses, such as 400 Bad Request and 401            */
/* Unauthorized, which are equipped to handle additional data        */
/* and customized error messages.                                    */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse: For sending HTTP responses                        */
/* - json: Module for JSON encoding                                  */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
import json
from typing import Union
from django.http import HttpResponse, HttpRequest

"""
file that includes request status codes for when things go wrong

NOTE: these need to include **kwargs to work properly in other views
"""


def bad_request_400(err_mssg: str="",**kwargs) -> None:
    response = HttpResponse(f"400 Bad Request => {err_mssg}")
    response.status_code = 400
    
    return response
    

#please make it pretty front end :)
def invalid_request_401(request,**kwargs):
    response = HttpResponse('Unauthorized') #better 401 page here
    
    response.status_code = 401

#please make it pretty front end :)
def invalid_request_401(request : HttpRequest, response_data : Union[dict,str] = 'Unauthorized') -> HttpResponse:
    """
    Description
    -----------
    Page to handles any attempt to access a page without valid credentials

    Parameters
    ----------
    - request (HttpRequest): The client request information

    Optional Parameters
    -------------------
    - response_data (dict | str): The details of the request and how it's handled

    Returns
    -------
    - HttpResponse: The error 401 information to return to the client

    Example Usage
    -------------
    
    >>> @User.Decorators.require_logged_in_mentee(invalid_request_401)
    'Unauthorized'

    Authors
    -------
    
    """
    response = None
    
    if type(response_data) == str:
        response = HttpResponse(response_data)
    elif type(response_data) == dict:
        response = HttpResponse(json.dumps(response_data))
    
    response.status_code = 401
    return response