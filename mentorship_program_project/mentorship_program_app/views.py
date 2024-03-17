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
ARVP  3/10/2024  Added ProfileImg and Organization imports
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

from .view_routes.status_codes import bad_request_400

from .models import User
from .models import Interest
from .models import Mentor
from .models import Mentee

from .models import MentorshipRequest
from .models import SystemLogs
from .models import ProfileImg
from .models import Organization



from .view_routes.navigation import landing


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
        'interestlist': Interest.objects.all(),

        'pronounlist1': ['he', 'she', 'they'],
        'pronounlist2': ['him', 'her', 'them'],

        'companytypelist': [
            'Manufacturing',
            'Computer Science', 
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
        'interestlist':  Interest.objects.all(),
        
        'menteeEmailMessage': "You MUST use your SVSU.EDU email address.",
        
        'pronounlist1': ['he', 'she', 'they'],
        'pronounlist2': ['him', 'her', 'them'],
        
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

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))

# TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING --ANTHONY PETERS
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
    session_user = User.from_session(request.session)

    # Create storge for list
    unaffiliated_mentors = []
    organizations = []
    mentees = []

    ## NEED TO DETETECT AND INCLUDE DEACTIVATED MAYBE STYLING TOO 

    # role = session_user.get_database_role_string
    # TESTING
    role = User.Role.ADMIN

    # Preset flags to false
    user_super_admin_flag = False
    user_admin_flag = False
    user_organization_admin_flag = False

    # TODO COMMENTED OUT TILL TESTING SIGNED IN
    # # Check if user is a suoer admin
    # if (session_user.is_super_admin()):
    #     user_super_admin_flag = True

    # Check if user is a admin
    if (role == User.Role.ADMIN):
        user_admin_flag = True

    # Check if user is a organization admin
    for organization in Organization.objects.all():
        for admin in organization.admins.all():
            if (session_user == admin):
                # Store organization infomation
                user_organization_admin_flag = True
                user_organization = organization

    # Load from database based on role
    # Check if user is an super admin or admin
    if (user_super_admin_flag | user_admin_flag):
        # Get all mentee, mentor, and organization data from database
        user_management_mentee_data = Mentee.objects
        user_management_mentor_data = Mentor.objects
        user_management_organizations_data = Organization.objects

    # TODO NEED TO CHECK THROUGH ORG ADMIN LIST FOR MENTORS (CHECK BELOW))

    # Check if user is an organization admin
    elif (user_organization_admin_flag):
        # Get all mentee data, only the admin's organization, and mentor data from within the organization
        user_management_mentee_data = Mentee.objects
        user_management_mentor_data = Mentor.objects


        # TODO NEED TO FIX USER MANAGEMENT ORG DATA
        user_management_organizations_data = user_organization

    else:
        user_management_mentee_data = []
        user_management_mentor_data = []
        user_management_organizations_data = []
        
    # Check if there is organization data to cycle through
    if not (user_management_organizations_data == []):
        # Cycle through organizations storing organization data
        for organization in user_management_organizations_data.all():
            # Create admin list for organization
            admin_list = []

            # Cycle through admins of organization
            for organization_admin in organization.admins.all():
                # Remove mentor from unafiiaited mentor group
                user_management_mentor_data.remove(organization_admin)

                # TODO WILL NEED TO TEST UNSURE IF WORKING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Get mentorship objects if possible    
                mentorships = MentorshipRequest.objects.filter(mentor=mentor.account)

                # TODO NEED TO TEST 
                # # Determine if organization admin is a super admin and set flag
                # if (organization_admin.is_super_admin()):
                #     mentor_super_admin_flag = True
                # else:
                #     mentor_super_admin_flag = False

                # Set current mentor amount from mentorship object's count
                current_mentees = mentorships.count()
                
                # Check if mentor has at least 1 mentorship
                if (current_mentees > 0):
                    # Create an empty list for mentees
                    mentee_list = []

                    # Loop through mentorship list, adding mentees to mentee list
                    for current_mentorship in mentorships:
                        mentee_list.append(current_mentorship.mentee)
                else:
                    # Set mentee list to none
                    mentee_list = None

                # TODO WILL NEED TO SET UP FOR NOW ASSUMING ALL ARE ACTIVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Check if mentee is deactivated
                deactivated = False

                # Add needed mentee info to organization list
                admin_list.append(
                    {
                        'account': mentor.account,
                        'mentees': mentee_list,
                        'current_mentees': current_mentees,
                        'max_mentees': mentor.int_max_mentees,
                        # 'mentor_super_admin_flag': mentor_super_admin_flag,
                        'deactivated': deactivated
                    }
                )

                # FOR TESTING
                print()
                print(mentor.account)

            # FOR TESTING
            print(organization.str_org_name)

            organizations.append(
                {
                    'organizations': organizations,
                    'name': organization.str_org_name,
                    'admin_list': admin_list
                }
            )

    # Check if there is mentor data to cycle through
    if not (user_management_mentor_data == []):
        # Cycle through unaffiliated mentors storing mentor data
        for mentor in user_management_mentor_data.all():
            # Get mentorship objects if possible    
            mentorships = MentorshipRequest.objects.filter(mentor=mentor.account)

            # TODO NEED TO TEST 
            # # Determine if mentor is a super admin and set flag
            # if (mentor.account.is_super_admin()):
            #     mentor_super_admin_flag = True
            # else:
            #     mentor_super_admin_flag = False

            # Determine if mentor is a admin and set flag
            if (mentor.account.str_role == User.Role.ADMIN):
                mentor_admin_flag = True
            else:
                mentor_admin_flag = False            

            # Set current mentor amount from mentorship object's count
            current_mentees = mentorships.count()
            
            # Check if mentor has at least 1 mentorship
            if (current_mentees > 0):
                # Create an empty list for mentees
                mentee_list = []

                # Loop through mentorship list, adding mentees to mentee list
                for current_mentorship in mentorships:
                    mentee_list.append(current_mentorship.mentee)
            else:
                # Set mentee list to none
                mentee_list = None

            # TODO WILL NEED TO SET UP FOR NOW ASSUMING ALL ARE ACTIVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Check if mentee is deactivated
            deactivated = False

            # Add needed mentee info to mentees list
            unaffiliated_mentors.append(
                {
                    'account': mentor.account,
                    'mentees': mentee_list,
                    'current_mentees': current_mentees,
                    'max_mentees': mentor.int_max_mentees,
                    # 'mentor_super_admin_flag': mentor_super_admin_flag,
                    'mentor_admin_flag': mentor_admin_flag,
                    'deactivated': deactivated
                }
            )

    # Check if there is mentee data to cycle through
    if not (user_management_mentee_data == []):
        # Cycle through mentee storing mentee data
        for mentee in user_management_mentee_data.all():
            # Get mentorship object if possible    
            mentorship = MentorshipRequest.objects.filter(mentee=mentee.account)
            
            # Check if mentee is include in any MentorshipReqiest objects and set has_mentor and mentor accordingly
            if (mentorship):
                has_mentor = True
                mentor = mentorship[0].mentor
            else:
                has_mentor = False
                mentor = None

            # TODO WILL NEED TO SET UP FOR NOW ASSUMING ALL ARE ACTIVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Check if mentee is deactivated
            deactivated = False

            # Add needed mentee info to mentees list
            mentees.append(
                {
                    'account': mentee.account,
                    'mentor': mentor,
                    'has_mentor': has_mentor,
                    'deactivated': deactivated
                }
            )

    context = {
        'mentees': mentees,
        'unaffiliated_mentors': unaffiliated_mentors,
        'organizations': organizations,
        'role': role,
        'user_super_admin_flag': user_super_admin_flag,
        'user_admin_flag': user_admin_flag,
        'user_organization_admin_flag': user_organization_admin_flag
    }

    return HttpResponse(template.render(context,request))



@security.Decorators.require_login(invalid_request_401)
def logout(request):
    if security.logout(request.session):
        return landing(request)
    #TODO: redirect this to a correct form ||||| probably done - Tanner
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
        response = HttpResponse(json.dumps({"warning":"The username/password you have entered is incorrect."}))
        response.status_code = 401
        return response
 
    #valid login
    if not security.set_logged_in(request.session,User.objects.get(cls_email_address=uname)):
        response = HttpResponse(json.dumps({"warning":"You are currently pending approval"}))
        response.status_code = 401
        return response

    user = User.objects.get(cls_email_address=uname)
    user.str_last_login_date = date.today()
    user.save()

    # record logs
    SystemLogs.objects.create(str_event=SystemLogs.Event.LOGON_EVENT, specified_user=user)



    response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
    return response

# view goes to currently static approve/delete mentors page
def change_settings(request):
    context = {}
    template = loader.get_template('settings.html')
    return HttpResponse(template.render(context,request))

# view goes to currently static view reported users page
def admin_reported_users(request):
    context = {}
    template = loader.get_template('admin/admin_reported_users.html')
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


