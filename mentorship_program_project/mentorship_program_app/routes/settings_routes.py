"""
/*********************************************************************/
/* FILE NAME: settings_routes.py                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew and Ben?                                       */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to enable users to manage their notification    */
/* settings and view their settings page with ease, enhancing user   */
/* experience by providing control over the notifications they       */
/* receive and ensuring they can access and adjust their settings    */
/* directly through the platform.                                    */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file includes functions to toggle user notification settings */
/* and render the user settings page, allowing for dynamic interaction */
/* on the client side without the need for page refresh.             */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For handling HTTP requests                         */
/* - HttpResponse: For sending HTTP responses                        */
/* - loader: For loading HTML templates                              */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

from django.http import HttpResponse, HttpRequest
from django.template import loader
from mentorship_program_app.models import *
from .status_codes import invalid_request_401
from utils import security
from .emails import *
from ..models import *

def toggle_notifications(req : HttpRequest, status : bool):
    """
    Toggles the notification settings for the logged-in user based on the provided status.

    Parameters:
    - req (HttpRequest): The request object containing session details.
    - status (bool): A boolean value indicating the desired notification state (True for on, False for off).

    Returns:
    - HttpResponse: A response with a message indicating the updated status.
    """
    user = User.from_session(req.session)
    if status == "true":
        user.bln_notifications = True
    elif status == "false":
        user.bln_notifications = False
    user.save()

    return HttpResponse("Status Updated")

@security.Decorators.require_login(invalid_request_401)
def change_settings(request):
    """
    Renders the settings page for the user, allowing them to view and change their settings.

    Parameters:
    - request (HttpRequest): The request object containing session details.

    Returns:
    - HttpResponse: Renders the 'settings.html' template with current settings context.
    """
    user = User.from_session(request.session)
    template = loader.get_template('settings.html')
    context = {"bln_notifications_on": user.bln_notifications,
               "is_mentee": user.is_mentee()}
    return HttpResponse(template.render(context,request))