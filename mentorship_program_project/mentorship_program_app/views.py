import json
from typing import Union

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
def invalid_request_401(request,response_data : Union[dict,str] = 'Unauthorized'):
    response = None
    
    if type(response_data) == str:
        response = HttpResponse(response_data)
    elif type(response_data) == dict:
        response = HttpResponse(json.dumps(response_data))
    
    response.status_code = 401
    return response

"""
creates or deletes a request for the given mentor from the current mentee that is logged in
"""
@User.Decorators.require_loggedin_mentee(invalid_request_401)
def request_mentor(request):
    if request.method == 'POST':
        
        #attempt to parse out data from the post response
        mentee_id = security.get_user_id_from_session(request.session)
        action = request.POST.get("create",False)
        mentor_id = request.POST.get("mentor_id",None)

        if mentor_id == None:
            return invalid_request_401(request,{"error":"invalid mentor id"})


        bool_response = False
        if action:
            bool_response = MentorshipRequest.create_request(mentor_id, mentee_id)
        else:
            bool_response = MentorshipRequest.remove_request(mentor_id, mentee_id)
        
        #we failed to make a response
        if not bool_response:
            return invalid_request_401(request,{"error":"failed to create mapping"})
    
    #if we get here the method on the request was not post
    #which means we get invalid data
    return invalid_request_401(request,{"error","must use post method"})



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
    security.set_logged_in(request.session,User.objects.get(clsEmailAddress=uname).id)
    response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
    return response

# view goes to currently static approve/delete mentors page
def mentor_judgement(request):
    context = {}
    template = loader.get_template('pending_mentors.html')
    return HttpResponse(template.render(context,request))


