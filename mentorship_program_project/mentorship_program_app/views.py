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
WJL   3/14/2024  Finished adding comments and updating to standards
"""

#standard python imports
import json
from typing import Union, Dict
from datetime import date

from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.utils import timezone

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
from .models import *
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


def big_move(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads the account_creation_0_mentor HTML with an empty context

    Parameters
    ----------
    - req (HttpRequest): The request information including items to be rendered
        into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The rendered view template with the empty context and
        HttpRequest information

    Example Usage
    -------------
    
    >>> path('big_move/', views.big_move, name='big move')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def the_big_move(req):
    template = loader.get_template('sign-in card/mentor/account_creation_sign_up_choices_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def the_second_move(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads the single_page_mentee HTML with an empty context

    Parameters
    ----------
    - req (HttpRequest): The request information including items to be rendered
        into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The rendered view template with the empty context and
        HttpRequest information

    Example Usage
    -------------
    
    >>> path('the_second_move/', views.the_second_move, name='the second move')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/single_page_mentee.html')
    context = {}
    return HttpResponse(template.render(context, req))

def register_mentee(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads the single_page_mentee HTML with an full hard-coded context. Does not
    actually process any information.

    Parameters
    ----------
    - req (HttpRequest): The request information including items to be rendered
        into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The rendered view template with the context and
        HttpRequest information

    Example Usage
    -------------
    
    >>> path('register_mentee/', views.register_mentee, name='Mentee Registration')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/single_page_mentee.html')
    if not Interest.objects.exists():
        Interest.create_default_interests()
    
    # import os
    # print(os.getcwd())
    country_codes : Dict
    with open('mentorship_program_app/view_routes/countries.json', 'r') as file:
        country_codes = json.load(file)
        country_codes = sorted(country_codes, key=lambda item: item["dial_code"])
        
    
    context = {
        'interestlist':  Interest.objects.all(),
        
        'menteeEmailMessage': "You MUST use your SVSU.EDU email address.",
        
        'pronounlist1': ['', 'he', 'she', 'they'],
        'pronounlist2': ['', 'him', 'her', 'them'],
        
        'country_codes' : country_codes,
        
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
        
        # C:\Users\andyp\OneDrive\Documents\GitHub\mentorship-program\mentorship_program_project
    
    country_codes : Dict
    with open('mentorship_program_app/view_routes/countries.json', 'r') as file:
        #country_codes = json.load(file).items() # dict(sorted(json.load(file).items(), key=lambda item: item[1].dial_code))
        country_codes = json.load(file)
        country_codes = sorted(country_codes, key=lambda item: item["dial_code"])
    #sorted(json.load(file))
    context = {
        'interestlist': Interest.objects.all(),

        'pronounlist1': ['', 'he', 'she', 'they'],
        'pronounlist2': ['', 'him', 'her', 'them'],
        
        'country_codes' : country_codes,

        'companytypelist': [
            'Manufacturing',
            'Computer Science', 
            'Math?'],
            
        'experiencelist': [
            '0-4 years',
            '5-9 years', 
            '10+ years',
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



def faq(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads the FAQ page with an empty context

    Parameters
    ----------
    - req (HttpRequest): The request information including items to be rendered
        into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The rendered view template with the empty context and
        HttpRequest information

    Example Usage
    -------------
    
    >>> path('help/faq/', views.faq, name='Frequently Asked Questions')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('faq.html')
    context = {}
    return HttpResponse(template.render(context, req))

# Pho Post handler for landing-page login card
def landing_post(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Redirects to the dashboard or landing pages depending on if the request
    method is POST or not (respectively)

    Parameters
    ----------
    - req (HttpRequest): The request information that has the request method

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponseRedirect: The HttpResponse for the redirected page URL

    Example Usage
    -------------
    
    >>> path('landing/', views.landing_post, name='Landing')
    HttpResponseRedirect

    Authors
    -------
    
    """
    if req.method == 'POST':
        return redirect('dashboard')
    else:
        return redirect('landing')

def profile_card(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads a profile card with a context consisting of ambiguous items

    Parameters
    ----------
    - req (HttpRequest): The request information including items to be rendered
        into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The HTML completed with items and any request information

    Example Usage
    -------------
    
    >>> path('profile_card/', views.profile_card, name='Profile Card')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('dashboard/profile-card/mentor_card.html')
    
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))

# TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING --ANTHONY PETERS
def role_selection(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders a role selection page

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('role_selection/', views.role_selection, name='Select Your Role')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/shared/role_selection.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_mentee(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the mentee account activation page

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentee_activation/', views.account_activation_mentee, name=
            'Mentee Account Activation')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/mentee/account_activation_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_invalid_mentee(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the account activation page for an invalid mentee with a
    hard-coded email in the context

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentee_activation/', views.account_activation_invalid_mentee,
            name='Invalid Mentee Activation')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/mentee/account_activation_invalid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_valid_mentee(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the account activation page for a valid mentee with a
    hard-coded email in the context

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentee_activation/', views.account_activation_valid_mentee,
            name='Valid Mentee Activation')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/mentee/account_activation_valid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_mentor(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the account activation page for an mentor

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentor_activation/', views.account_activation_mentor,
            name='Mentor Activation')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
from django.shortcuts import get_object_or_404

def get_mentor_data_from_mentor(mentor : 'Mentor',session_user : 'User')->dict:
    """
    convinece function that returns mentor data for the front end to use,
    I would muchly recommend going through the mentor objects themselfs if possible, but if this 
    is the prefered method this function makes it easier to work with :)
    """
    mentor_data = {
        'account': mentor,
        'id': str(mentor),
        #if you need the id mentor.account.id has it built in, so you don't need to pass it around twice,
        #still if you feel its better here uncomment :)
        #'id': str(mentor.account.id), #str(mentor.account), 
        
        #TODO:
        # we didn't see any usage usage of this while exploring, we also simplified the python
        # a bit to make it clearer what exactly this was passing over, we left the trailing , if
        # its needed anywhere (didn't see anything erroring with this commented out though)
        # if its still needed uncomment it :)
        # -dk
        'mentees': ",".join([str(m.account) for m in mentor._mentee_set.all()]),
        'current_mentees': mentor.mentee_set.count(),
        'max_mentees': mentor.int_max_mentees,

        # 'mentees': mentee_list,
        'mentor_admin_flag': session_user.is_super_admin() #auto caches :)
    }
    return mentor_data

def admin_user_management(request):
    '''
    Modified: 04/06/2024 Tanner K.
    -   Added functionality for org admins to access page. Primary change is organization 
        creation is directly tied to the boolean bl_user_org_admin and an if/elif block. 
    '''
    
    template = loader.get_template('admin/user_management.html')
    session_user = User.from_session(request.session)

    # Create storge for list
    organizations = []
    mentees = []

    # Create var for checking if user is org admin
    bl_user_org_admin = False

    # Load from database based on role
    # Check if user is an admin
    if (session_user.is_super_admin()):
        print_debug("loading with role admin")
        # Get all mentee, mentor, and organization data from database
        user_management_mentee_data = Mentee.objects
        user_management_mentor_data = Mentor.objects
        user_management_organizations_data = Organization.objects

        orgs = user_management_organizations_data.select_related(
                                            "admin_mentor"
                                ).prefetch_related(
                                                    "mentor_set",
                                                    "mentor_set___mentee_set",
                                                    "mentor_set__account",
                                                    "mentor_set___mentee_set__account",
                                                    "mentor_set__administered_organizations"
                                                    )

    # Check if user is an organization admin
    elif (session_user.is_an_org_admin()):
        print_debug("hello from the organization admin side of things UwU")
        # TODO NEED TO SET UP TO GET ONLY DATA THAT IS NEEDED FOR THAT ORG, ONLY MENTORS WITHIN ORG AND METEES REALTED TO THEM
        # MAYBE FILTER MENTORS BY ORG AND METEES BY MENTORS WITHIN ORG
        
        bl_user_org_admin = True

        # Get all mentee data, only the admin's organization, and mentor data from within the organization
        # user_management_mentee_data = Mentee.objects
        # user_management_mentor_data = Mentor.objects

        #TODO: you can be admin of more than one organization so get will error since it expects a single return value,
        #this should be a filter instead of a git, ill chage it if I get to it in time with optimization, but ima leave this note
        #here for others or incase I forget -dk
        organization = Organization.objects.get(admin_mentor_id=session_user.mentor)
        user_management_mentee_data = Mentee.objects.filter(mentor__organization=organization)
        user_management_mentor_data = Mentor.objects.filter(organization=organization)

        user_management_organizations_data = organization

        orgs = [organization]

        # return HttpResponse(organization, mentees_with_mentors_in_organization)

    else:
        return bad_request_400("Access Denied")


    # Cycle through organizations
    for organization in orgs:
        # Inizilize empty list for mentors and admins
        org_admin = None
        mentor_list = []
        
        if organization.admin_mentor != None:
            org_admin = get_mentor_data_from_mentor(organization.admin_mentor,session_user)

        organizations.append(
            {
                'organization': organization,
                'id': str(organization),
                'name': organization.str_org_name,
                'admin_list': [org_admin] if org_admin != None else [], #this def does not need to be a list now
                                                                        #unless we want to re-listify admins which we could do
                'mentor_list':  [
                                            get_mentor_data_from_mentor(m,session_user) for m in 
                                            organization.mentor_set.all() 
                                            if org_admin == None or organization.admin_mentor.id != m.id
                                ]
            }
        )

    #TODO dk:  make this prefetch data so we don't query like a horse in the desert without water that gets to an oasis its currently midnight he;p
    mentee_query = user_management_mentee_data.all().prefetch_related("account","mentor")
    for mentee in mentee_query:
        # Add needed mentee info to mentees list
        mentees.append({
            'account': mentee,
            'id': str(mentee),
            'mentor': mentee.mentor
        })

    context = {
        'mentees': mentees,
        'unaffiliated_mentors': [
                                    get_mentor_data_from_mentor(m,session_user) for m in 
                                    
                                    user_management_mentor_data.annotate(org_count=Count("organization")).filter(org_count=0).prefetch_related(
                                        "mentee_set","account","mentee_set__account"
                                        )
                                 ],
        'organizations': organizations,
        'role': session_user.str_role,

        'session_user_account': session_user,
        'organization_counter': Organization.objects.count(),

        'user_admin_flag': session_user.is_super_admin(),
        'user_organization_admin_flag': session_user.is_an_org_admin()
    }

    render = template.render(context,request)

    return HttpResponse(render)



@security.Decorators.require_login(invalid_request_401)
def logout(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Logs the current user out of the system, given they are already logged in

    Parameters
    ----------
    - request (HttpRequest): The request information containing the needed
        session information

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: A plaintext HttpResponse with a simple success or failure
        message

    Example Usage
    -------------
    
    >>> path('logout/', views.logout, name='Goodbye!')
    "logged out!"

    Authors
    -------
    
    """
    if security.logout(request.session):
        return redirect("/")
    #TODO: redirect this to a correct form ||||| probably done - Tanner
    response = HttpResponse("an internal error occured, unable to log you out, STAY FOREVER")
    response.status_code = 500
    return response



#login stuff

def login_uname_text(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Logs in a user, records the sign in, and redirects to the dashboard.

    Parameters
    ----------
    - request (HttpRequest): The request information containing the user's entered
        credentials

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: Response containing either an error code for an invalid
        login attempt or the redirect to the dashboard for a success.

    Example Usage
    -------------
    
    >>> path('login/', views.login_uname_text,
            name='')
    HttpResponse

    Authors
    -------
    
    """
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

    user.str_last_login_date = timezone.now()
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
    user = User.from_session(request.session)
    template = loader.get_template('settings.html')
    context = {"bln_notifications_on": user.bln_notifications}
    return HttpResponse(template.render(context,request))

# view goes to currently static view reported users page
def admin_reported_users(request):
    template = loader.get_template('admin/admin_reported_users.html')

    user_reports_dict = UserReport.get_unresolved_reports_grouped_by_user()
    context = {"user_reports_dict": user_reports_dict}
    return HttpResponse(template.render(context,request))

# view goes to mentor_group_view
def mentor_group_view(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the mentorship group page

    Parameters
    ----------
    - req (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentorship_group/', views.mentor_group_view,
            name='Your Mentorship Group')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template('group_view/mentor_group_view.html')
    context = {}
    return HttpResponse(template.render(context, req))


# development only views, these should be removed before production
# still if they are forgotten they should automatically redirect
# when not in DEBUG mode

@security.Decorators.require_debug(invalid_request_401)
def profile_picture_test(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders the user profile pictures, given that you are in debug
    mode. Additionally sanitized the blacklist properties for all users.

    Parameters
    ----------
    - request (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The fully rendered HTML page

    Example Usage
    -------------
    
    >>> path('mentee_activation/', views.account_activation_invalid_mentee,
            name='Inavlid Mentee Activation')
    HttpResponse

    Authors
    -------
    
    """
    context = {
                "users":[
                    u.sanitize_black_properties() for u in User.objects.all()
                ]
            }
    
    template = loader.get_template('dev/user_images.html')
    
    return HttpResponse(template.render(context,request))

@security.Decorators.require_login(invalid_request_401)
@security.Decorators.require_debug(invalid_request_401)
def is_logged_in_test(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Returns a simple message, given that the user is logged in and in debug
    mode.

    Parameters
    ----------
    - request (HttpRequest): Unused, but required by Django

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The object containing the plaintext message

    Example Usage
    -------------
    
    >>> path('logged_in_test/', views.is_logged_in_test, name='Logged In.')
    "you are currently logged in!"

    Authors
    -------
    
    """
    return HttpResponse("you are currently logged in!")



@security.Decorators.require_debug(invalid_request_401)
def test_database_setup(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Calls the database test function and returns a message on success, given
    that the user is in debug mode

    Parameters
    ----------
    - request (HttpRequest): Unused, but required by Django

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The object containing the plaintext message

    Example Usage
    -------------
    
    >>> path('test_db/', views.test_database_setup, name='Test Finished')
    "finished test successfully"

    Authors
    -------
    
    """
    development.test_database()
    return HttpResponse('finished test successfully')



@security.Decorators.require_debug(invalid_request_401)
def generate_random_user_data(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Calls the random data generator and returns a message on success, given
    that the user is in debug mode

    Parameters
    ----------
    - request (HttpRequest): Unused, but required by Django

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The object containing the plaintext message

    Example Usage
    -------------
    
    >>> path('data_gen/', views.generate_random_user_data,
            name='Generation Finished')
    "finished generating user data, enjoy controlling the populus :D"

    Authors
    -------
    
    """
    development.print_debug('running the function')
    development.populate_database_with_random_users()
    return HttpResponse('finished generating user data, enjoy controlling the populus :D')

@security.Decorators.require_debug(invalid_request_401)
def populate_default_interest_values(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Calls the database interest population function and returns a message on
    success, given that the user is in debug mode

    Parameters
    ----------
    - request (HttpRequest): Unused, but required by Django

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The object containing the plaintext message

    Example Usage
    -------------
    
    >>> path('populate_interests/', views.populate_default_interest_values,
            name='Interests Populated')
    "finished populating interests in the database!"

    Authors
    -------
    
    """
    development.print_debug("[*] generating interests in the database...")
    development.populate_database_with_interests()
    development.print_debug("[*] finished genereating interests! Enjoy the data :)")
    return HttpResponse("finished populating interests in the database!")

@security.Decorators.require_debug(invalid_request_401)
def delete_users(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    After confirming deletion in console, deletes all users from the database
    and returns a message on success, given that the user is in debug mode

    Parameters
    ----------
    - request (HttpRequest): Unused, but required by Django

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The object containing the plaintext message

    Example Usage
    -------------
    
    >>> path('delete_users/', views.delete_users, name='Deleted All Users')
    N
    "canceled action!"

    NOTE: Unsure if I showed the console input correctly, or if it needs to be
    shown at all.
    
    Authors
    -------
    
    """
    development.print_debug("[*] are you sure you want to replace all users?")
    if input("(y/n)> ").lower() == 'y':
        User.objects.all().delete()
        return HttpResponse("deleted all user sucessfully >:]")
    return HttpResponse("canceled action!")

@security.Decorators.require_debug(invalid_request_401)
def test_login_page(request : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Loads and renders a demo login page, given the user is in debug mode

    Parameters
    ----------
    - request (HttpRequest): The request information including any items to be
        rendered into the template

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The render HTML file

    Example Usage
    -------------
    
    >>> path('test_login_page/', views.test_login_page, name='It Works!')
    HttpResponse

    Authors
    -------
    
    """
    template = loader.get_template("dev/test_login.html")
    return HttpResponse(template.render({},request))