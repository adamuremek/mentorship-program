"""
FILE NAME: views.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED:

-------------------------------------------------------------------------------
FILE PURPOSE:
Defines all views used on the website.

-------------------------------------------------------------------------------
COMMAND LINE PARAMETER LIST (In Parameter Order):
(NONE)

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NONE)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
(NONE)

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO     WHEN     WHAT
WJL   3/3/2024   Added file header comment and updating to doc standards
"""

#standard python imports
import json
from typing import Union
from datetime import date

from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import render, redirect

from utils import development
from utils.development import print_debug
from utils import security

from .models import User
from .models import Interest
from .models import Mentor
from .models import MentorshipRequest


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

@User.Decorators.require_logged_in_mentee(invalid_request_401)
def request_mentor(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Creates or deletes a mentorship request for a given mentor from the current
    mentee, given that they are signed in.

    Parameters
    ----------
    - request (HttpRequest): The request information with the relevant
        mentorship request creation/deletion details

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The results of the operation. Currently uses a placeholder.

    Example Usage
    -------------
    
    >>> path('request_mentor/', views.request_mentor, name='request mentor')
    "Something Happened!"

    Authors
    -------
    
    """

    str_mentor_id = "mentor_id"
    #Init the variable.
    bool_response = False

    if request.method == 'POST':
        
        #attempt to parse out data from the post response
        mentee_id = security.get_user_id_from_session(request.session)
        action = request.POST.get("create",False)
        mentor_id = request.POST.get("mentor_id",None)

        #Get the data from the POST request.
        data = request.POST        
        int_mentee_id = security.get_user_id_from_session(request.session)
        
        #Insert the request into the database.
        bool_response = MentorshipRequest.create_request(data.get(str_mentor_id), int_mentee_id)

        if bool_response:
            #Request was added to the database.
            return HttpRequest("Something happened!") #PLACEHOLDER - REMOVE WHEN CHANGED WITH REAL DATA plz
        else:
            #Request was NOT added to the database.
            return HttpRequest("Something happened!") #PLACEHOLDER - REMOVE WHEN CHANGED WITH REAL DATA plz  
    else:
        #PLACEHOLDER - REMOVE WHEN CHANGED WITH REAL DATA plz
        return HttpRequest("Something happened!")



# -------------------- <<< Big Move stuff >>> -------------------- #
# - Will delete later


def BIGMOVE(req):
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def THEBIGMOVE(req):
    template = loader.get_template('sign-in card/single_page_mentor.html')
    context = {
        'interestlist': [
            'Artificial Intelligence', 
            'Computer Graphics', 
            'Data Structures & Algorithms',
            'Networking',
            'Operating Systems',
            'Embedded Systems',
            'Cloud Computing',
            'Software Engineering',
            'Distrubuted Systems',
            'Game Development',
            'Cybersecruity',
            'System Analysis'],

        'pronounlist': ['he', 'she', 'they'],

        'companytypelist': [
            'Manufacturing',
            'Comptuer Science', 
            'Math?'],
            
        'experiencelist': [
            '0 years',
            '0-2 years', 
            '2-5 years'],

        'useragreement': 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." + 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." +
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",

    }
    return HttpResponse(template.render(context, req))

def THESECONDMOVE(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    context = {}
    return HttpResponse(template.render(context, req))

def register_mentee(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    context = {
        'interestlist': [
            'Artificial Intelligence', 
            'Computer Graphics', 
            'Data Structures & Algorithms',
            'Networking',
            'Operating Systems',
            'Embedded Systems',
            'Cloud Computing',
            'Software Engineering',
            'Distrubuted Systems',
            'Game Development',
            'Cybersecruity',
            'System Analysis'],
        
        'pronounlist': ['he', 'she', 'they'],
        
        'useragreement': 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." + 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." +
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",

    }
    return HttpResponse(template.render(context, req))

def register_mentor(req):
    template = loader.get_template('sign-in card/mentor/account_creation_sign_up_choices_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

# --- #
# --- #
# --- #



def faq(req):
    template = loader.get_template('faq.html')
    context = {}
    return HttpResponse(template.render(context, req))

# Pho Post handler for landing-page login card
def landingPost(req):
    if req.method == 'POST':
        return redirect('dashboard')
    else:
        return redirect('landing')

def profileCard(req):
    template = loader.get_template('dashboard/profile-card/mentor_card.html')
    
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

#please make pretty front end we love you :D
def home(req):

    return HttpResponse('theres no place me')

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))

# TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING
def role_selection(request):
    template = loader.get_template('sign-in card/shared/role_selection.html')
    context = {}
    return HttpResponse(template.render(context, request))


def account_activation_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_invalid_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_invalid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_valid_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_valid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))

def admin_user_management(request):
    template = loader.get_template('admin/user_management.html')
    context = {
        #TODO NEED TO ADD SOME DUMMY INFO
    }
    return HttpResponse(template.render(context,request))\



@security.Decorators.require_login(invalid_request_401)
def logout(request):
    if security.logout(request.session):
        return HttpResponse("logged out!")
    
    #TODO: redirect this to a correct form
    response = HttpResponse("an internal error occured, unable to log you out, STAY FOREVER")
    response.status_code = 500
    return response



#login stuff

def login_uname_text(request):
    login_data = json.loads(request.body.decode("utf-8"))

    uname    = login_data["username"] if "username" in login_data else None
    password = login_data["password"] if "password" in login_data else None
    
    #even though these are print debug printing passwords makes me nervous
    #print_debug("uname " + uname)
    #print_debug("password " + password)


    if not User.check_valid_login(uname,password):
        response = HttpResponse(json.dumps({"warning":"invalid creds"}))
        response.status_code = 401
        return response
 
    #valid login
    security.set_logged_in(request.session,User.objects.get(cls_email_address=uname).id)
    user = User.objects.get(cls_email_address=uname)
    user.str_last_login_date = date.today()
    user.save()

    response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
    return response

# view goes to currently static approve/delete mentors page
def mentor_judgement(request):
    context = {}
    template = loader.get_template('pending_mentors.html')
    return HttpResponse(template.render(context,request))

# view goes to mentor_group_view
def mentor_group_view(req):
    template = loader.get_template('group_view/mentor_group_view.html')
    context = {}
    return HttpResponse(template.render(context, req))


# development only views, these should be removed before production
# still if they are forgotten they should automatically redirect
# when not in DEBUG mode

@security.Decorators.require_debug(invalid_request_401)
def profile_picture_test(request):
    context = {
                "users":[
                    u.sanitize_black_properties() for u in User.objects.all()
                ]
            }
    
    template = loader.get_template('dev/user_images.html')
    
    return HttpResponse(template.render(context,request))

@security.Decorators.require_login(invalid_request_401)
@security.Decorators.require_debug(invalid_request_401)
def is_logged_in_test(request):
    return HttpResponse("you are currently logged in!")



@security.Decorators.require_debug(invalid_request_401)
def test_database_setup(request):
    development.test_database()
    return HttpResponse('finished test sucesfully')



@security.Decorators.require_debug(invalid_request_401)
def generate_random_user_data(request):
    development.print_debug('running the function')
    development.populate_database_with_random_users()
    return HttpResponse('finished generating user data, enjoy controlling the populus :D')

@security.Decorators.require_debug(invalid_request_401)
def populate_default_interest_values(request):
    development.print_debug("[*] generating interests in the database...")
    development.populate_database_with_interests()
    development.print_debug("[*] finished genereating interests! Enjoy the data :)")
    return HttpResponse("finished populating interests in the database!")

@security.Decorators.require_debug(invalid_request_401)
def delete_users(request):
    development.print_debug("[*] are you sure you want to replace all users?")
    if input("(y/n)> ").lower() == 'y':
        User.objects.all().delete()
        return HttpResponse("deleted all user sucessfully >:]")
    return HttpResponse("canceled action!")

@security.Decorators.require_debug(invalid_request_401)
def test_login_page(request):
    template = loader.get_template("dev/test_login.html")
    return HttpResponse(template.render({},request))


