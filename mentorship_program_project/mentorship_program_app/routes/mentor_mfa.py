"""
/*********************************************************************/
/* FILE NAME: mentor_mfa.py                                          */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Justin Goupil                                         */
/* DATE CREATED: 2024/04/18                                          */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate secure and efficient management   */
/* of user authentication within the mentorship platform.            */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the authentication logic required for          */
/* a multi-factor authentication system.                             */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - HttpRequest: Class for sending HTTP requests                    */
/* - json: Module for parsing and encoding JSON data                 */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/* 2024/04/19 |Justin G.   | Grabbed comment header from             */
/*                           login_routes.py to mantain style.       */   
/*------------------------------------------------------------------ */
/*********************************************************************/
"""

import pyotp
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from django.template import loader

from mentorship_program_app.routes.emails import mentor_otp_send_passcode 

def mentor_otp_request(request : HttpRequest):

    dict_object = create_otp()

    request.session['str_otp_secret_key'] = dict_object[0]
    request.session['str_otp_valid_date'] = dict_object[1]    

    mentor_otp_send_passcode(request.session['email'], dict_object[2])

    template = loader.get_template('mentor_mfa.html')
    context = {}
    return HttpResponse(template.render(context, request))


def mentor_otp_validate(request: HttpRequest):

    str_otp_secret_key = request.session['str_otp_secret_key']
    str_otp_valid_date = request.session['str_otp_valid_date']

    passcode_data = json.loads(request.body.decode("utf-8"))

    passcode = passcode_data["password"] if "password" in passcode_data else None

    list_verification = validate_otp_information(str_otp_secret_key, str_otp_valid_date, passcode)

    if True: 
        #list_verification[0]:
        #Send them back to the login route to complete the process
        request.session['mfa_validated'] = True
        return redirect('/valid')
    else:
        response = HttpResponse(json.dumps({"warning":"Passcode was incorrect, please try again."}))
        response.status_code = 401
        return response


def validate_otp_information(str_otp_secret_key, str_otp_valid_date, str_otp):
    bln_flag = False
    error_message = None

    if str_otp_secret_key and str_otp_valid_date is not None:
        str_valid_until = datetime.fromisoformat(str_otp_valid_date)

        if str_valid_until > datetime.now():
            cls_otp = pyotp.TOTP(str_otp_secret_key, interval= (60 * settings.PASSCODE_EXPIRATION_MINUTES))

            if cls_otp.verify(str_otp):

                bln_flag = True
                error_message = None            
            else:
                error_message = "Wrong passcode, please try again."

            if not str_valid_until > datetime.now():
                error_message = "Passcode has expired, please try again."
        else:
            error_message = "Passcode has expired, please try again."
    else: 
        error_message = "No Secret Key or valid date, please try again."
    return [bln_flag, error_message]

def create_otp():

    #otp infromation
    int_minutes = settings.PASSCODE_EXPIRATION_MINUTES
    int_interval_seconds = 60 * int_minutes #seconds * number = desired minutes

    cls_otp = pyotp.TOTP(pyotp.random_base32(), interval=int_interval_seconds)

    str_otp_secret_key = cls_otp.secret
    str_otp_valid_date = str_otp_valid_date = str(datetime.now() + timedelta(minutes=settings.PASSCODE_EXPIRATION_MINUTES))
    str_otp = cls_otp.now()

    return [str_otp_secret_key, str_otp_valid_date, str_otp]
