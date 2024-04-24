"""
/*********************************************************************/
/* FILE NAME: password_routes.py                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew P and Tanner W                                 */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate secure and efficient management   */
/* of user authentication within the mentorship platform, including  */
/* functionalities such as password resets, email verification, and  */
/* other security features.                                          */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the routes and logic for password management   */
/* and user authentication through email verification within the     */
/* mentorship platform. It supports functionalities such as          */
/* resetting passwords, checking if an email is associated with an   */
/* account, and updating passwords.                                  */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - JsonResponse: Class for sending JSON responses                  */
/* - loader, Template: Utilities for rendering HTML templates        */
/* - ObjectDoesNotExist: Exception for handling non-existent objects */
/* - render: Function to render HTML pages with context              */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
import json
from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from mentorship_program_app.models import *
from utils import security
from .emails import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import *


@csrf_exempt
def reset_request(req: HttpRequest):
    '''
     Description
     ___________
     a route that creates a token and emails it the given email,
     the token can be used to reset the email on another view

     Paramaters
     __________
        req : HttpRequest - django http request

     Returns
     _______
        HttpResponse containing a descriptive message of what happened
     
     Example Usage
     _____________
        >>> reset_request(req)

        

     >>> 
     Authors
     _______
     Tanner Williams 🦞
    '''


    email = req.POST.get('email', None)
    
    try:
        user = User.objects.get(cls_email_address=email.lower())
    except ObjectDoesNotExist:
        return HttpResponse(False)
    
    valid, message, token = PasswordResetToken.create_reset_token(user_id=user.id)
    if not user.is_mentee():
        reset_token_email(req, recipient=user.cls_email_address, token=token) # Pass req along with recipient email and token
    return HttpResponse(True)



@csrf_exempt
def reset_password(req : HttpRequest):
    '''
     Description
     ___________
     route takes in a new password and previously sent token and verifys said token,
     then replaces the password for the user

     Paramaters
     __________
        req : HttpRequest - django http request

     Returns
     _______
        HttpResponse containing a descriptive message of what happened
     
     Example Usage
     _____________
        >>> reset_password(req)

        

     >>> 
     Authors
     _______
     Tanner Williams 🦞
    '''

    new_password = req.POST.get('new-password', None)
    token = req.POST.get('token', None)
   


    valid, message = PasswordResetToken.validate_and_reset_password(token=token,new_password=new_password)

    # redirect to the page the request came from
    return JsonResponse({'valid': valid, 'message': message})   
    
def request_reset_page(req, token=None):
    '''
    Updated: 3/22/2024 Tanner K.
    Updated route to include context as navbar will not load without it.
    Old code is commented below.
    '''

    # template = loader.get_template('reset_page.html')
    # return HttpResponse(template.render())

    template: Template = loader.get_template('reset_page.html')
    context: dict = {}
    
    return HttpResponse(template.render(context, req))

@csrf_exempt
def check_email_for_password_reset(request):
    '''
     Description
     ___________
     a route called from the password reset modal
     that checks to see if an account exist with a certain email 

     Paramaters
     __________
        req : HttpRequest - django http request

     Returns
     _______
        JsonResponse if account exist
     
     Example Usage
     _____________
        >>> check_email_for_password_reset(request)
         
        JsonResponse({'exists': User.objects.filter(cls_email_address=email).exists()})

        

     >>> 
     Authors
     _______
     Tanner Williams 🦞
    '''
    email = request.GET.get('email', None)

    data = {
        'exists': User.objects.filter(cls_email_address=email).exists() #                                          🦞
    }

    return JsonResponse(data) 

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        exists = User.objects.filter(cls_email_address=email).exists()
        return JsonResponse({'exists': exists})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def change_password(req : HttpRequest):
    '''
    Description
    -----------
    Function to change the password of the currently logged-in user. It validates the old password, generates a new salt, hashes the new password with this salt, updates the user's password details, and saves these changes to the database.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the old and new passwords submitted through a form.

    Returns
    -------
    HttpResponse
        Renders the settings page with a message indicating whether the password was successfully updated or if the old password was invalid.

    Authors
    -------
    - Andrew P
    '''
    # Retrieve old and new passwords from POST request
    old_password = req.POST["old-password"]
    new_password = req.POST["new-password"]
    user = User.from_session(req.session)
    # Check if the old password is valid
    if not user.check_valid_password(old_password): 
           return render(req, 'settings.html', {'message':"Invalid Password"})
    # Hash the new password with the newly generated salt
    generated_user_salt = security.generate_salt()
    user.str_password_hash = security.hash_password(new_password, generated_user_salt)
    user.str_password_salt = generated_user_salt
    user.save()

    # redirect to the page the request came from
    return render(req, 'settings.html', {'message':"Password Updated"})