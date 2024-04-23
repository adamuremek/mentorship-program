"""
/*********************************************************************/
/* FILE NAME: login_routes.py                                      */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: David K. and Quinn                                    */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate secure and efficient management   */
/* of user authentication within the mentorship platform, utilizing  */
/* both SAML-based and traditional username/password mechanisms.     */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file handles the complex authentication logic required for   */
/* supporting SAML logins and traditional username/password logins.  */
/* It also manages user logout procedures, ensuring proper handling  */
/* of session terminations and user activity logging.                */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for parsing and encoding JSON data                 */
/* - redirect: Function to redirect the user to a different URL      */
/* - timezone: Utilities to handle timezone-related functionalities  */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/* 2024-04-14 | Tanner     | Added SAML authentication functionality */
/* 2024-04-15 | Dev Team   | Integrated username/password validation */
/* 2024-04-19 |Justin G.   | Modified login_uname_text to support otp*/
/*                         | Created complete_login to support MFA   */
/*********************************************************************/
"""

import json
from django.http import HttpResponse
from django.shortcuts import redirect
from mentorship_program_app.models import *
from .status_codes import invalid_request_401
from utils import security
from .emails import *
from django.utils import timezone
from ..models import *
from mentorship_program_app.routes.mentor_mfa import *

# sucessful saml logins redirect here
# the built in django user will be logged in, but our user will not be, and it might not even exist yet (first time sign in)
def saml_login(request):
    user = request.user

    # Invalid saml login. Probably cannot get to this page, but good to be sure
    if not user:
        #TODO: add a error message
        return redirect('landing')
    
    if not User.objects.filter(cls_email_address=user.email).exists():
        #TODO: The registration flow still needs some work, but it at least functions now
        return redirect('/register/mentee')

    # User exists, log them in
    user = User.objects.get(cls_email_address=user.email)
    if not user.bln_active:
        user.bln_active = True
        user.save() 

    if user.bln_account_disabled:
        response = HttpResponse(json.dumps({"warning":"Your account has been disabled"}))
        response.status_code = 401
        return response
    security.set_logged_in(request.session,user)
    return redirect('/dashboard')

def login_uname_text(request):
    login_data = json.loads(request.body.decode("utf-8"))

    uname    = login_data["username"] if "username" in login_data else None
    password = login_data["password"] if "password" in login_data else None
    
    if not User.check_valid_login(uname,password):
        response = HttpResponse(json.dumps({"warning":"The username/password you have entered is incorrect."}))
        response.status_code = 401
        return response       
    
    request.session['email'] = uname
    request.session['mfa_validated'] = False

    #redirects to the mentor one time password route
    response = HttpResponse(json.dumps({"new_web_location":'/mentor/2fa'}))
    return response

def complete_login(request):
        
        uname = request.session['email']
        request.session['email'] = None

        if not request.session['mfa_validated']:
            request.session['mfa_validated'] = False
            return redirect("/")

        #valid login
        if not security.set_logged_in(request.session,User.objects.get(cls_email_address=uname)):
            response = HttpResponse(json.dumps({"warning":"You are currently pending approval"}))
            response.status_code = 401
            return response
        #disabled account
        if User.objects.get(cls_email_address=uname).bln_account_disabled:
            response = HttpResponse(json.dumps({"warning":"Your account has been disabled"}))
            response.status_code = 401
            return response
    
        user = User.objects.get(cls_email_address=uname)

        user.str_last_login_date = timezone.now()
        # if the user deactivated their own account, reactivate it
        if not user.bln_active and not user.bln_account_disabled:
            user.bln_active = True
        user.save()
        # record logs
        SystemLogs.objects.create(str_event=SystemLogs.Event.LOGON_EVENT, specified_user=user)

        response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
        return response  

@security.Decorators.require_login(invalid_request_401)
def logout(request):
    if security.logout(request.session):
         # if the user is logged in with django's auth (through saml)
        if request.user.is_authenticated:
            # log them out through saml
            return redirect("/saml2/logout")
        return redirect("/")
    #TODO: redirect this to a correct form ||||| probably done - Tanner
    response = HttpResponse("an internal error occured, unable to log you out, STAY FOREVER")
    response.status_code = 500
    return response

