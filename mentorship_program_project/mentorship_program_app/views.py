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
from django.db.models import Count, Q
from django.shortcuts import render, redirect


from utils import development
from utils.development import print_debug
from utils import security

from .view_routes.status_codes import bad_request_400

from .models import User
from .models import Interest
from .models import Mentor
from .models import UserReport
from .models import Mentee

from .models import MentorshipRequest
from .models import SystemLogs
from .models import ProfileImg
from .models import Organization

# from .models import MentorReports # (Deprecated??)



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
    template = loader.get_template('sign-in card/mentor/account_creation_sign_up_choices_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def THESECONDMOVE(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    context = {}
    return HttpResponse(template.render(context, req))

def register_mentee(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    if not Interest.objects.exists():
        Interest.create_default_interests()
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

# def register_mentor(req):
#     template = loader.get_template('sign-in card/mentor/account_creation_sign_up_choices_mentor.html')
#     context = {}
#     return HttpResponse(template.render(context, req))

def register_mentor(req):
    template = loader.get_template('sign-in card/single_page_mentor.html')
    if not Interest.objects.exists():
        Interest.create_default_interests()
    context = {
        'interestlist': Interest.objects.all(),

        'pronounlist1': ['he', 'she', 'they'],
        'pronounlist2': ['him', 'her', 'them'],

        'companytypelist': [
            'Manufacturing',
            'Computer Science', 
            'Math?'],
            
        'experiencelist': [
            '0-5 years',
            '5-10 years', 
            '15+ years',
            ],

        'useragreement': 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." + 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." +
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",

    }
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
    
from django.shortcuts import get_object_or_404

def admin_user_management(request):
    template = loader.get_template('admin/user_management.html')
    session_user = User.from_session(request.session)

    # Create storge for list
    unaffiliated_mentors = []
    organizations = []
    mentees = []

    # Preset flags to false
    user_super_flag = False
    user_admin_flag = False
    user_organization_admin_flag = False

    # Determine role of session user
    role = session_user.str_role    

    # Determine session user's id
    session_user_id = str(session_user)

    # Load from database based on role
    # Check if session user is an admin
    if (role == "Admin"):
        # Get all mentee, mentor, and organization data from database
        user_management_mentee_data = Mentee.objects
        user_management_mentor_data = Mentor.objects
        user_management_organizations_data = Organization.objects
        
        # Set role flag
        user_admin_flag = True

        # Check and set user super flag if session user is a super admin
        user_super_flag = session_user.is_super_admin()
    
    # Check if user is an organization admin
    elif (session_user.is_mentor() and Organization.objects.filter(admins=session_user.mentor).exists()):
        # TODO NEED TO SET UP TO GET ONLY DATA THAT IS NEEDED FOR THAT ORG, ONLY MENTORS WITHIN ORG AND METEES REALTED TO THEM
        # MAYBE FILTER MENTORS BY ORG AND METEES BY MENTORS WITHIN ORG

        # Get only the organization admin's mentor and mentee data from within the organization
        organization = Organization.objects.get(admins=session_user.mentor)
        # mentees_with_mentors_in_organization = Mentee.objects.filter(mentor__organization=organization)

        user_management_organizations_data = organization

        user_management_mentee_data = Mentee.objects.filter(mentor__organization=organization)
        user_management_mentor_data = Mentor.objects.filter(organization=organization)

        # Set role flag
        user_organization_admin_flag = True
        
        # return HttpResponse(organization, mentees_with_mentors_in_organization)

    else:
        # Get no mentee, mentor, or organization data from database
        user_management_mentee_data = []
        user_management_mentor_data = []
        user_management_organizations_data = []

        # return HttpResponse("Access Denied")

    # Cycle through organizations
    for organization in user_management_organizations_data.all():
        # Inizilize empty list for mentors and admins
        admin_list = []
        mentor_list = []

        organizations.append(
            {
                'organization': organization,
                'id': str(organization),
                'name': organization.str_org_name,
                'admin_list': admin_list,
                'mentor_list': mentor_list
            }
        )

    # Cycle through mentors
    for mentor in user_management_mentor_data.all():
        # Inizlize empty list 
        mentee_list = ""

        # Get mentees set from mentor object
        mentee_set = mentor.mentee_set.all()

        # Check if mentee set is not empty then create a string that is comma seperated from queryset
        if (mentee_set.count() > 0):
            for mentee in mentee_set:
                mentee_list = mentee_list + str(mentee.account) + ","

        # Determine if mentor is a admin and set flag
        if (role == User.Role.ADMIN):
            mentor_admin_flag = True
        else:
            mentor_admin_flag = False

        # Create mentor data
        mentor_data = {
            'account': mentor.account,
            'id': str(mentor.account),
            'mentees': mentee_list,
            'current_mentees': mentee_set.count(),
            'max_mentees': mentor.int_max_mentees,
            'mentor_admin_flag': mentor_admin_flag
        }

        # Check if mentor is a part of any organizations
        if (mentor.organization.count() > 0):
            # Cycle and attach mentor to organizations they are part of
            for mentor_organization in mentor.organization.all():
                # Cycle thorugh organization list searching for organization that matches mentor's
                for organization in organizations:
                    # Check if mentor organization matches organization
                    if (mentor_organization == organization["organization"]):
                        # Check if organization admin
                        if (mentor == mentor_organization.admin_mentor):

                            print(mentor_organization.admin_mentor)

                        # if (mentor.is_admin_of_organization(mentor_organization)):
                            # Attach mentor to admin list
                            organization["admin_list"].append(mentor_data)

                        else: 
                            # Attach mentor to mentor list
                            organization["mentor_list"].append(mentor_data)

                        break
        else:
            # Attach mentor to unaffiliated list
            unaffiliated_mentors.append(mentor_data)

    # Cycle through mentees
    for mentee in user_management_mentee_data.all():
        # Add needed mentee info to mentees list
        mentees.append({
            'account': mentee.account,
            'id': str(mentee.account),
            'mentor': mentee.mentor
        })



    # print(session_user)

    # for org in organizations:
    #     print(org)

    # for mentor in unaffiliated_mentors:
    #     print(mentor)

    # for mentee in mentees:
    #     print(mentee)



    context = {
        'mentees': mentees,
        'unaffiliated_mentors': unaffiliated_mentors,
        'organizations': organizations,
        'role': role,
        'session_user_account': session_user_id,
        'user_super_flag': user_super_flag,
        'user_admin_flag': user_admin_flag,
        'user_organization_admin_flag': user_organization_admin_flag
    }

    return HttpResponse(template.render(context,request))



@security.Decorators.require_login(invalid_request_401)
def logout(request):
    if security.logout(request.session):
        return redirect("/")
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

    if User.objects.get(cls_email_address=uname).bln_account_disabled:
        response = HttpResponse(json.dumps({"warning":"Your account has been disabled"}))
        response.status_code = 401
        return response

    user = User.objects.get(cls_email_address=uname)
    user.str_last_login_date = date.today()
    # if the user deactivated their own account, reactivate it
    if not user.bln_active and not user.bln_account_disabled:
        user.bln_active = True
    user.save()
    # record logs
    SystemLogs.objects.create(str_event=SystemLogs.Event.LOGON_EVENT, specified_user=user)



    response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
    return response
    

# view goes to currently static approve/delete mentors page
@security.Decorators.require_login(invalid_request_401)
def change_settings(request):
    
    template = loader.get_template('settings.html')
    context = {}
    return HttpResponse(template.render(context,request))

# view goes to currently static view reported users page
def admin_reported_users(request):
    template = loader.get_template('admin/admin_reported_users.html')

    user_reports_dict = UserReport.get_unresolved_reports_grouped_by_user()
    context = {"user_reports_dict": user_reports_dict}
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


