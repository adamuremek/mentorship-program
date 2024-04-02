import json
import re
import inspect
from collections.abc import Callable
from datetime import date

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader, Template
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from utils.development import print_debug
from .emails import *
from ..views import login_uname_text
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

"""
TODO: if a mentee wants to register to be a mentor, possibly have them sign up again
through the mentor sign up route and update their role user entry in the DB to mentor when approved

TODO: Have mentors fill out more information when signing up so the admin get a better 

TODO: Send email when mentor is approved/declined

"""



def is_ascii(s: str) -> str:
    '''
    Description
    -----------
    Check if a given string is made up of only ASCII characters.
    
    Parameters
    ----------
    - s (str): The string which is being evaluated for ASCII only characters.
    
    Returns
    -------
    - str: An empty string ("") if the string only contains ASCII characters. Otherwise, 
    a message string is returned informing that the string contains non-ASCII characters.
    
    Example Usage
    -------------
    
    >>> is_ascii("Goodbye World!")
    ""
    >>> is_ascii("💩")
    "String contains non-ASCII characters."
    
    Authors
    -------
    Adam U. :)
    '''
    
    #Standard ASCII character set ranges from 0 to 127
    return "" if all(ord(c) < 128 for c in s) else "String contains non-ASCII characters."

def contains_sql_injection_risk(input_string: str) -> str:
    '''
    Description
    -----------
    Check if a given string contains SQL query information that could be used
    to perform as SQL injection attack.
    
    Parameters
    ----------
    - input_string (str): The string which will be evaluated for SQL tokens.
    
    Returns
    -------
    - str: An empty string ("") if the string does not contain any SQL tokens. Otherwise,
    a message string is returned informing of the possible SQL tokens within the provided
    string.
    
    Example Usage
    -------------
    
    >>> contains_sql_injection_risk("Real programmers dont comment their code")
    ""
    >>> contains_sql_injection_risk("Uh oh very stinky payload ' OR 1=1 --")
    "String contains possible SQL tokens."
    
    Authors
    -------
    Adam U. 8==D~
    '''
    
    # List of patterns to check for
    patterns = [
        r"(--|\#|\*|;|=)",
        r"(SELECT\s|INSERT\s|DELETE\s|UPDATE\s|DROP\s|EXEC\s|UNION\s|ALTER\s|CREATE\s|INDEX\s|REPLACE\s)",
        r"('|\")"
    ]
    
    # Check if any of the patterns are found in the input_string
    for pattern in patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return "String contains possible SQL tokens."  # SQL injection risk found
    
    return ""  # No SQL injection risk found


VALIDATE_REQ_BODY_ERR_MSSG = "The 'validate_request_body' \
decorator is typically only used on route callback functions \
that need one or more of its body's string values verified."

def __validate_request_body(req_callback: Callable, *body_args: str, **kwargs) -> Callable:
    def wrapper(*args,**kwargs):
        #The calling function should have at least one argument.
        if len(args) < 1:
            raise Exception(f"Function {req_callback.__name__} has no arguments! {VALIDATE_REQ_BODY_ERR_MSSG}")
        
        #The first argument of the calling function must be an HttpRequest for it to be a route callback.
        if not isinstance(args[0], HttpRequest):
            raise Exception(f"Function {req_callback.__name__} is not a route callback! {VALIDATE_REQ_BODY_ERR_MSSG}")
        
        #The decorator must have at least one parameter given to validate.
        if len(body_args) < 1:
            raise Exception(f"No body argurments for validation were provided!")
        
        #Get the request from the calling route callback function.
        req: HttpRequest = args[0]
        
        if req.method == "POST":
            #Filter the post request's data dict with the parameters provided into the decorator
            body_dict: dict = {key:req.POST[key] for key in body_args if key in req.POST}
            err_mssg: str = ""
            
            #Validate each parameter's value
            for value in body_dict.values():
                err_mssg = is_ascii(value)
                err_mssg = contains_sql_injection_risk(value)
                
                if err_mssg != "":
                    return bad_request_400(f"{err_mssg} | problem_string: {value}")
        
        return req_callback(*args,**kwargs)
    
    return wrapper

def validate_request_body(*args: str,**kwargs):
    return lambda func: __validate_request_body(func, *args,**kwargs)

@validate_request_body("fname", "lname", "pronouns", "email", "phone-number", "password")
def register_mentor(req: HttpRequest):
    
    #TODO return organization and job title as well
    '''
    Description
    -----------
    Function that will allow people to request to be a mentor.
    
    Parameters
    ----------
    - req : HttpRequest
    req should contain email (str), password (str), firstname (str), lastname (str), phone_number (str), pronouns (str), jobTitle (str), organization (str)
    
    Returns
    -------
    - str: Email {email} already exsists!
    - str: Registration request successful! We'll get back to ya!
    - str: Bad :(
    
    Example Usage
    -------------
    
    >>> reqister_mentor(req)
    "Email {email} already exsists!"
    
    >>> reqister_mentor(req)
    Registration request successful! We'll get back to ya!
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    '''
    if req.method == "POST":
        incoming_email: str = req.POST["email"]
        incoming_plain_text_password = req.POST["password"]

        # create a new user in the database with the role "Pending"
        pending_mentor_object = Mentor.create_from_plain_text_and_email(incoming_plain_text_password, incoming_email)
        
        # check if the account is already registered
        if pending_mentor_object == User.ErrorCode.AlreadySelectedEmail:
            return HttpResponse(f"Email {incoming_email} already exsists!")

        organization = None
        if(not Organization.objects.filter(str_org_name=req.POST["organization"]).exists()):
            organization = Organization.objects.create(str_org_name=req.POST["organization"])
            organization.admins.add(pending_mentor_object)
            organization.save()

        else:
            organization = Organization.objects.get(str_org_name=req.POST["organization"])
            
        pending_mentor_object.account.cls_email_address = incoming_email
        pending_mentor_object.account.str_first_name = req.POST["fname"]
        pending_mentor_object.account.str_last_name = req.POST["lname"]
        pending_mentor_object.account.str_phone_number = req.POST["phone"]
        pending_mentor_object.account.str_preferred_pronouns = req.POST["pronouns1"] + '/' + req.POST["pronouns2"]

        #were not getting the data from the incoming form
        #if this is a thing we need to keep track of we should prolly send it
        #idk tho do whatevs -dk
        #str_gender = str_gender,


        user_mentor = User.objects.get(cls_email_address = incoming_email)
        
        pending_mentor_object.str_job_title =  req.POST["jobTitle"]
        pending_mentor_object.str_experience = req.POST["experience"]
        pending_mentor_object.organization.add(organization)

        parsed_user_interests = [
                                    Interest.get_or_create_interest(interest) for interest in req.POST.getlist("selected_interests")
                                 ]


        pending_mentor_object.account.save()
        pending_mentor_object.save()

        for interest in parsed_user_interests:
            pending_mentor_object.account.interests.add(interest)


        pending_mentor_object.save()

        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_REGISTER_EVENT, specified_user= User.objects.get(id=user_mentor.id))
        mentor_signup_email(pending_mentor_object.account.cls_email_address)
        template: Template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
        ctx = {}
        
        return HttpResponse(template.render(ctx, req))
        
    else:
        return HttpResponse("Bad :(")
    

def register_mentee(req: HttpRequest):
    
    '''
    Description
    -----------
    Function that will allow people to request to be a mentee.
    
    Parameters
    ----------
    - req : HttpRequest
    req should contain email (str), password (str), firstname (str), lastname (str), phone_number (str), pronouns (str)
    
    Returns
    -------
    - str: Email {email} already exsists!
    - HttpResponseRedirect:  ̶R̶e̶g̶i̶s̶t̶r̶a̶t̶i̶o̶n̶ ̶r̶e̶q̶u̶e̶s̶t̶ ̶s̶u̶c̶c̶e̶s̶s̶f̶u̶l̶!̶ ̶W̶e̶'̶l̶l̶ ̶g̶e̶t̶ ̶b̶a̶c̶k̶ ̶t̶o̶ ̶y̶a̶! now redirects the new user to their dashboard
    - str: Bad :(
    
    Example Usage
    -------------
    
    >>> reqister_mentee(req)
    "Email {email} already exsists!"
    
    >>> reqister_mentee(req)
    Registration request successful! We'll get back to ya!
    
     Edits
    -------------
    -changed the response from plain text html to a login and redirect

    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    Tanner W. 🦞
    '''
    if req.method == "POST":
        incoming_email: str = req.POST["email"]
        incoming_plain_text_password = req.POST["password"]


        # create a new user in the database with the role "Pending"
        pending_mentee_object = Mentee.create_from_plain_text_and_email(incoming_plain_text_password, incoming_email)
        
        # check if the account is already registered
        if pending_mentee_object == User.ErrorCode.AlreadySelectedEmail:
            return HttpResponse(f"Email {incoming_email} already exsists!")
            
        pending_mentee_object.account.cls_email_address = incoming_email
        pending_mentee_object.account.str_first_name = req.POST["fname"]
        pending_mentee_object.account.str_last_name = req.POST["lname"]
        pending_mentee_object.account.str_preferred_pronouns = req.POST["pronouns1"] + '/' + req.POST["pronouns2"]

        parsed_user_interests = [
                                    Interest.get_or_create_interest(interest) for interest in req.POST.getlist("selected_interests")
                                ]

        


        for interest in parsed_user_interests:
            pending_mentee_object.account.interests.add(interest)

        
        pending_mentee_object.account.save()
        pending_mentee_object.save()

        user_mentee = User.objects.get(cls_email_address = incoming_email)
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, specified_user= User.objects.get(id=user_mentee.id))



        ##adds info to req with correct data names for the login function to work
        req._body = json.dumps({"username": incoming_email, "password": incoming_plain_text_password}).encode("utf-8")
        ##logins in the user
        login_uname_text(req)
        ##redirects to the dashboard
        redirect_url = "/dashboard"
        redirect_response = HttpResponseRedirect(redirect_url)
        return redirect_response
    else:
        return HttpResponse("Bad :(")

def view_pending_mentors(req: HttpRequest):
    '''
    Description
    -----------
    Function that returns all of the pending mentors
    
    Parameters
    ----------
    - req : HttpRequest
    
    Returns
    -------
     HttpResponse: HTTP response containing the pending mentors
    
    Example Usage
    -------------
    
    >>> view_pending_mentors(req)
    Name: {first_name} {last_name} Email: {email} id: {user.id} || Name: {first_name} {last_name} Email: {email} id: {user.id} || ...
    

    Authors
    -------
    Adam U. ♣
    Andrew P.
    '''
    
    #TODO Verify youre an admin


    template = loader.get_template('pending_mentors.html')
    # Get all mentors who are still pending
    pending_mentors = User.objects.filter(str_role="MentorPending")
    
    context = {"pending_mentors" : pending_mentors}
    
    return HttpResponse(template.render(context, req))


def change_mentor_status(req: HttpRequest):
    '''
    Description
    -----------
    Function to change the status of a mentor from pending to approved or declined.
    
    Parameters
    ----------
    - req : HttpRequest: HTTP request object containing mentor status change data.
    
    Returns
    -------
    HttpResponse: HTTP response confirming the status change.
    
    Example Usage
    -------------
    This function is typically called via an HTTP POST request with JSON data containing the mentor's ID and the desired status change.
    
    >>> change_mentor_status(req)
    "user {mentor_id}'s status has been changed to: {status}"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    '''
    #TODO Verify you're an admin

    if req.method != "POST":
        HttpResponse("wtf")

    # Extract mentor ID and status from request data
    mentor_id = req.POST["mentor_id"]
    status = req.POST["status"]
    
    # Retrieve user object based on ID
    user = User.objects.get(id=mentor_id)
    
    # Update user role and activation status based on provided status                                           
    if status == 'Approved':
        user.bln_active = True
        user.str_role = User.Role.MENTOR
        user.save()
        mentor_accepted_email(user.cls_email_address)      
    else:
        mentor_denied_email(user.cls_email_address)
        user.delete()
        
        
    # Save changes to user object
    
    # Redirect back to the view_pending page
    return redirect("/view_pending")


def disable_user(req:HttpRequest):
    '''
    Description
    -----------
    Function to disable a user by disabling their account.
    
    Parameters
    ----------
    - req : HttpRequest: HTTP request object containing a user who was disabled.
    
    Returns
    -------
    HttpResponse: HTTP response confirming the disable action.
    
    Example Usage
    -------------
    This function is typically called via an HTTP POST request with JSON data containing the user's ID and the confirmation of disable.
    
    >>> disable_user(req)
    "user {id} has been disabled"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    '''
    post_data = json.loads(req.body.decode("utf-8"))
        
    id = post_data["id"] if "id" in post_data else None

    # Validate user id 
    if(id == None):
        return HttpResponse("User doesn't exist")
    
    # Get the user and set their disabled field to True
    user = User.objects.get(id=id)
    user.bln_account_disabled = True
    
    # Save changes to user object
    user.save()
    if(user.str_role == "Mentee"):
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTEE_DEACTIVATED_EVENT, specified_user= User.objects.get(id=user.id))
    else:
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_DEACTIVATED_EVENT, specified_user= User.objects.get(id=user.id))
    return HttpResponse(f"user {id}'s status has been changed to disabled")


def enable_user(req:HttpRequest):
    '''
    Description
    -----------
    Function to enable a user by enabling their account.
    
    Parameters
    ----------
    - req : HttpRequest: HTTP request object containing a user who was enabled.
    
    Returns
    -------
    HttpResponse: HTTP response confirming the enable action.
    
    Example Usage
    -------------
    This function is typically called via an HTTP POST request with JSON data containing the user's ID and the confirmation of enable.
    
    >>> enable_user(req)
    "user {id} has been enabled"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    '''
    post_data = json.loads(req.body.decode("utf-8"))
        
    id = post_data["id"] if "id" in post_data else None

    # Validate user id 
    if(id == None):
        return HttpResponse("User doesn't exist")
    
    # Get the user and set their disabled field to False
    user = User.objects.get(id=id)
    user.bln_account_disabled = False
    
    # Save changes to user object
    user.save()
    
    return HttpResponse(f"user {id}'s status has been changed to enabled")



@security.Decorators.require_login(bad_request_400)
def update_profile_img(user_id, new_pfp):
    '''
    Description
    -----------
    Function to update a user's profile image

    
    Parameters
    ----------
    -   req:HttpRequest: HTTP request object should contain the image
                         name that will be used to update the user's 
                         profile.
    
                         
    Returns
    -------
    HttpResponse: HTTP response confirming the modification to the user's profile
                  image.

                  
    Example Usage
    -------------
    This function is typically called using a POST request, which should have retrieved
    the name/location of an image file before it was invoked.

    >>> update_profile_img(req)
    "user {int_user_id}'s image profile has been SUCCESSFULLY modified"

    
    Authors
    -------
    🌟 Isaiah Galaviz 🌟
    '''
    page_owner_user = User.objects.get(id=user_id)

    #   If the name of the file is not valid (wrong file extension or insufficient name length),
    #   return an HttpResponse saying the user's profile was not modified.
    if new_pfp == None:
        return bad_request_400(f"User {user_id}'s image profile was NOT modified")
    elif len(new_pfp.name) < 5:
        return bad_request_400(f"File name was invalid. User {user_id}'s profile was NOT modified.")
    elif new_pfp.name.endswith(".png") == False:
        return bad_request_400(f"File name was invalid. User {user_id}'s profile was NOT modified.")
    elif new_pfp.name.endswith(".jpg") == False:
        return bad_request_400(f"File name was invalid. User {user_id}'s profile was NOT modified.")
    
    #   Otherwise, continue on with running the function.
    else:
        #   Check if a 'ProfileImg' instance exists that is associated
        #   with the user currently logged into the system.
        profile_img = ProfileImg.objects.get(user=page_owner_user)
        if profile_img == None:
            #   If not, create a new instance of the ProfileImg model 
            #   and store it in the program's database
            bool_flag = ProfileImg.create_from_user_id(int_user_id=user_id)
            #   Return a response saying the process did not go through, if so.
            if bool_flag == False:
                return bad_request_400(f"Something went wrong while trying to modify user {user_id}'s profile.")
            #   If the process did go through, get the newly created instance.
            profile_img = ProfileImg.objects.get(user=page_owner_user)

        #   Store the image name and save the image instance
        profile_img.img_title = new_pfp

        #   Take the name of the image file and store it in the user's ImageView.
        profile_img.img_profile = new_pfp
        profile_img.save()


@security.Decorators.require_login(bad_request_400)
def create_note (req : HttpRequest):
    """
    Description
    -----------
    This view creates and stores a note in the database 
    given a user id, title and body.

    Paramaters
    __________
    req (HttpRequest): Django Http request.

    Returns
    _______
    HttpResponse for data that is valid.
    HttpResponse for data that is invalid.
     
    Example Usage
    _____________
    >>> create_note(request)

    /path/to/route/

    Authors
    -------
    Justin Goupil
    Adam U.
    """

    #Grab the users current session
    user = User.from_session(req.session)
    # Get data
    str_title = req.POST["note-title"]
    str_public_body = req.POST["public-notes"]
    str_private_body = req.POST["private-notes"]
    # Make note
    Notes.create_note(user.id, str_title, str_public_body, str_private_body)

    return redirect(f"/universal_profile/{user.id}")

@security.Decorators.require_login(bad_request_400)
def update_note(req: HttpRequest):
    if req.method == "POST":
        #Grab current session user
        user = User.from_session(req.session)

        note_id = req.POST["note-id"]
        new_title = req.POST["note-title"]
        new_pub_body = req.POST["public-notes"]
        new_pvt_body = req.POST["private-notes"]

        Notes.update_note(note_id, new_title, new_pub_body, new_pvt_body)

    return redirect(f"/universal_profile/{user.id}")

@security.Decorators.require_login(bad_request_400)
def remove_note(req: HttpRequest):
    if req.method == "POST":

        #Grab current session user
        user = User.from_session(req.session)
        note_id = int(json.loads(req.body)["note-id"])

        Notes.remove_note(note_id)

    return redirect(f"/universal_profile/{user.id}")

#TODO uncomment this
#@security.Decorators.require_login(bad_request_400)
def view_mentor_by_admin(req: HttpRequest):
    """
    Description
    -----------
    This view allows an admin to view details of a mentor, including their profile information and interests.

    Parameters
    __________
    req (HttpRequest): Django Http request.

    Returns
    _______
    HttpResponse with mentor details if successful.
    HttpResponse indicating failure if mentor details cannot be retrieved.
     
    Example Usage
    _____________
    >>> view_mentor_by_admin(request)

    /view_mentor_by_admin

    Authors
    -------
    Andrew P.
    Adam U.
    Jordan A.
    """
    if req.method == "POST":
        mentor_id = req.POST["mentor_id"]
        template = loader.get_template('dashboard/profile-card/admin_viewing_pending_mentor.html')
        user = User.objects.get(id=mentor_id)
        mentor = Mentor.objects.get(account_id=mentor_id)
        organization = mentor.organization.get(mentor=mentor).str_org_name
        interests = user.interests.filter(user=user)
        
        user_interests = []
        for interest in interests:
            user_interests.append(interest.strInterest)

        context = {"first_name": user.str_first_name,
                   "last_name": user.str_last_name,
                   "job_title": mentor.str_job_title,
                   "organization": organization,
                   "user_interests": user_interests,
                   "experience" : mentor.str_experience,
                   "user" : user.sanitize_black_properties()
                   }
        return HttpResponse(template.render(context, req))

  
    return HttpResponse("eat my fat nuts!")


@security.Decorators.require_login(bad_request_400)
def group_view(req: HttpRequest):
    template = loader.get_template('group_view/mentor_group_view.html')
    signed_in_user = User.from_session(req.session)
    mentor_id = req.POST["id"]
    # the user object for the page owner
    page_owner_user = User.objects.get(id=mentor_id)
    # the mentor object for the page owner 
    page_owner_mentor = page_owner_user.mentor

    organization = page_owner_mentor.organization.get(mentor=page_owner_mentor).str_org_name

    interests = page_owner_user.interests.filter(user=page_owner_user)

    is_page_owner = signed_in_user == page_owner_user

    user_interests = []
    for interest in interests:
        user_interests.append(interest.strInterest)

    # had to preform a ritual to get this to work
    # give me the big bucks
    # honestly a christmas miracle this works, wowza
    # DO NOT TOUCH, ITS DANGEROUS
    mentees_for_mentor = page_owner_mentor.mentee_set.all()
    mentees_users_accounts = [mentee.account for mentee in mentees_for_mentor]



    context = {"signed_in_user": signed_in_user.sanitize_black_properties(),
               "is_page_owner": is_page_owner,
               "page_owner_user":page_owner_user,
               "page_owner_mentor" : page_owner_mentor,
               "organization": organization,
               "interests": user_interests,
               "mentees" : mentees_users_accounts
               }
    return HttpResponse(template.render(context,req))

@security.Decorators.require_login(bad_request_400)
def universalProfile(req : HttpRequest, user_id : int):
    
    profile_page_owner = None
    try:
        profile_page_owner = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return bad_request_400("user page does not exist")

    template = loader.get_template('group_view/combined_views.html')
    signed_in_user = User.from_session(req.session)
    signed_in_user.has_requested_this_user = signed_in_user.has_requested_user(profile_page_owner)
  
    
    # the user object for the page owner
    page_owner_user = User.objects.get(id=user_id)

    page_owner_go_fuck_yourself = getattr(page_owner_user, 'mentee' if page_owner_user.is_mentee else 'mentor', None)
    interests = page_owner_user.interests.filter(user=page_owner_user)
    is_page_owner = signed_in_user == page_owner_user
    user_interests = []
    for interest in interests:
        user_interests.append(interest)

    all_interests = Interest.objects.all()
    pendingList = []
    notes = None
    max_mentees = None
    num_mentees = None
    
    report_types = UserReport.ReportType.labels
    # get the pending mentorship requests for the page
    if page_owner_user.is_mentee():
        pendingRequests = MentorshipRequest.objects.filter(mentee_id=page_owner_user.id)
        try:
            mentees_or_mentor = []
            mentee = page_owner_go_fuck_yourself
            mentees_or_mentor.append(User.objects.get(id=mentee.mentor.account_id))
        except Exception:
            mentees_or_mentor = None
       
        for pending in pendingRequests:
            if pending.mentee_id != pending.requester:
                pendingList.append(User.objects.get(id=pending.mentor_id))
        
    elif page_owner_user.is_mentor():
        mentees_for_mentor = page_owner_user.mentor.mentee_set.all()
        mentees_or_mentor = [mentee.account for mentee in mentees_for_mentor]
    
        notes = Notes.get_all_mentor_notes(page_owner_user)
        pendingRequests = MentorshipRequest.objects.filter(mentor_id = page_owner_user.id)
        
        max_mentees = page_owner_user.mentor.int_max_mentees
        num_mentees = range(9, len(mentees_for_mentor)-1, -1) ##subtract one from length so they display properly online 🦞
        
        for pending in pendingRequests:
            if pending.mentor_id != pending.requester:
                pendingList.append(User.objects.get(id=pending.mentee_id))
             
            
    context = {
                "signed_in_user": signed_in_user.sanitize_black_properties(),
                "is_page_owner": is_page_owner,
                "page_owner_user":page_owner_user,
                "interests": user_interests,
                "page_owner_go_fuck_yourself": page_owner_go_fuck_yourself,
                "all_interests" : all_interests,
                "user_id" : user_id,
                "pending" : pendingList,
                "notes" : notes,
                "max_mentees" : max_mentees,
                "num_mentees" : num_mentees,
                "mentees_or_mentor" : mentees_or_mentor,
                "report_types" : report_types,
               }
    return HttpResponse(template.render(context,req))

@security.Decorators.require_login(bad_request_400)
def reject_mentorship_request(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    session_user = User.from_session(req.session)
    mentor_account = None
    try:
        mentor_account = User.objects.get(id=mentor_user_account_id)
    except ObjectDoesNotExist:
        return bad_request_400("mentor id is invalid!")

    if session_user.is_super_admin() or session_user.id == mentee_user_account_id or session_user.id == mentor_user_account_id:
        try:
            mentorship_request = MentorshipRequest.objects.get(
                                        mentor_id=mentor_user_account_id,
                                        mentee_id=mentee_user_account_id
                                        )
            try:
                mentorship_request.delete()
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            except:
                return bad_request_400("unable to create request!")

        except ObjectDoesNotExist:
            return bad_request_400("you do not have a request to accept!")
    return bad_request_400("permission denied!")

@security.Decorators.require_login(bad_request_400)
def accept_mentorship_request(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    session_user = User.from_session(req.session)
    mentor_account = None
    try:
        mentor_account = User.objects.get(id=mentor_user_account_id)
    except ObjectDoesNotExist:
        return bad_request_400("mentor id is invalid!")

    
    if session_user.is_super_admin() or session_user.id == mentee_user_account_id or session_user.id == mentor_user_account_id:
        try:
            mentorship_request = MentorshipRequest.objects.get(
                                        mentor_id=mentor_user_account_id,
                                        mentee_id=mentee_user_account_id
                                        )
            
            
            #we should never get here, but just in case
            #we should never get here, but just in case
            # if mentorship_request.is_accepted():
            #     return bad_request_400("you already accepted this request!")

            sucessful = None
            try:
                sucessful = mentorship_request.accept_request(session_user)
            except ValidationError:
                #this mentor has max mentees
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            
            if sucessful:
                return redirect(f"/universal_profile/{User.from_session(req.session).id}")
            
            return bad_request_400("unable to create request!")

        except ObjectDoesNotExist:
            return bad_request_400("you do not have a request to accept!")
    return bad_request_400("permission denied!")

def save_profile_info(req : HttpRequest, user_id : int):
    """
    Description
    ===========
    
    This route applies profile edits sent in the request to the respective proifle.

    Author
    ======
    Adam U. ( ͡° ͜ʖ ͡°) 

    """
    if req.method == "POST":
        #Get the user being modified
        page_owner_user = User.objects.get(id=user_id)

        #Change profile picture
        if "profile_image" in req.FILES:
            new_pfp = req.FILES["profile_image"]

            # update_profile_img(user_id, new_pfp)
            
            page_owner_user.profile_img.img.save(new_pfp.name, new_pfp)

        #Set the new interests
        new_interests: list = req.POST.getlist("selected_interests")
        interest_data = Interest.objects.filter(strInterest__in=new_interests)

        page_owner_user.interests.clear()
        page_owner_user.interests.add(*interest_data)

        # Set Max Mentees
        if page_owner_user.is_mentor():
            page_owner_user.mentor.int_max_mentees = req.POST["max_mentees"]
            page_owner_user.mentor.save()

        #Set the new bio
        page_owner_user.str_bio = req.POST["bio"]
        page_owner_user.save()
        

    return redirect(f"/universal_profile/{user_id}")


@security.Decorators.require_login(bad_request_400)
def create_mentorship(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse:
    """
    Description
    ___________
    creates a mentorship relation between the given mentor and mentee ids

    Authors
    _______
    David Kennamer .._..
    """
    session_user = User.from_session(req.session)

    session_user.create_mentorship_from_user_ids(mentee_user_account_id, mentor_user_account_id)

    return HttpResponse("created request sucessfully")

@security.Decorators.require_login(bad_request_400)
def delete_mentorship(req: HttpRequest, mentee_user_account_id):
    print(mentee_user_account_id)
    mentee = Mentee.objects.get(account_id=mentee_user_account_id)
    mentee.mentor_id = None
    mentee.save()
    # redirect to the page the request came from
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))



@security.Decorators.require_login(bad_request_400)
def request_mentor(req : HttpRequest,mentee_id : int,mentor_id : int)->HttpResponse:
    '''
     Description
     ___________
     view that creates a mentor request between a given mentor id 
     and mentee id

     Paramaters
     __________
        req : HttpRequest - django http request
        mentee_id : int - mentee id from the datbase, must be valid
        mentor_id : int - mentee id from the database, must be valid

     Returns
     _______
        HttpResponse containing a valid json ok signature or 401 error code for invalid data
     
     Example Usage
     _____________
        >>> request_mentor(request,mentee_id,mentor_id)

        /path/to/route/mentee_id/mentor_id

     >>> 
     Authors
     _______
     David Kennamer *^*
    '''
    user = User.from_session(req.session)
    print('Hello')
    
    
    #if you are a mentee you can only request for yourself
    if user.is_mentee():
        mentee_id : int = user.id
    elif user.is_mentor() and mentee_id == None:
        return bad_request_400("mentee id required for mentors")

    ##print_debug(user.has_requested_user(mentor_id))
    mentor_account = None
    mentee_account = None
    
    try:
        mentor_account = User.objects.get(id=mentor_id)
        mentee_account = User.objects.get(id=mentee_id)
    except ObjectDoesNotExist:
        return bad_request_400("invalid id detected!")
    
    if mentor_account == None or mentee_account == None:
        response = HttpResponse(json.dumps({"result":"unable to create request!"}))
        response.status_code = 400
        return response

    mentorship_request = MentorshipRequest.create_request(mentor_account.id,mentee_account.id)

    if mentorship_request: 
        mentorship_request.save() 
    else:
        print("this request already exists, IDENTITY CRISIS ERROR 🤿  ⛰️")

    ##print_debug(user.has_requested_user(mentor_id))
    return HttpResponse(json.dumps({"result":"created request!"}));


def change_password(req : HttpRequest):
    old_password = req.POST["old-password"]
    new_password = req.POST["new-password"]
    user = User.from_session(req.session)
    if not user.check_valid_password(old_password): 
           return render(req, 'settings.html', {'message':"Invalid Password"})
    
    generated_user_salt = security.generate_salt()
    user.str_password_hash = security.hash_password(new_password, generated_user_salt)
    user.str_password_salt = generated_user_salt
    user.save()

    # redirect to the page the request came from
    return render(req, 'settings.html', {'message':"Password Updated"})


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
        user = User.objects.get(cls_email_address=email)
    except ObjectDoesNotExist:
        return HttpResponse(False)
    
    valid, message, token = PasswordResetToken.create_reset_token(user_id=user.id)
    
    reset_token_email(req, recipient=user.cls_email_address, token=token) # Pass req along with recipient email and token
    print("email sent to: "+email)
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


def available_mentees(req: HttpRequest):
    template = loader.get_template('admin/available_mentees.html')
    added_mentees = None
    removed_mentees = None
    context = {}

    return HttpResponse(template.render(context,req))


def process_file(req: HttpRequest):
    template = loader.get_template('admin/available_mentees.html')
    
    if req.method == "GET":
        context = {'added': [], 'removed': [], 'file_name': ''}
        return HttpResponse(template.render(context, req))

    if req.method == 'POST' and 'fileUpload' in req.FILES:
        imported_file = req.FILES['fileUpload']
        whitelisted_and_present = []
        added_users = []
        all_whitelisted_emails = set(WhitelistedEmails.objects.values_list('str_email', flat=True))
        emails_in_file = set()
        try:
            # Read the content of the uploaded file
            file_content = imported_file.read().decode('utf-8').splitlines()

            for line in file_content:
                parts = line.strip().split('\t')
                if len(parts) < 3:
                    continue  # Skip lines that don't have at least three parts
                email, first_name, last_name = parts[0], parts[1], parts[2]
                user_tuple = (email, first_name, last_name)
                emails_in_file.add(user_tuple)

                if email in all_whitelisted_emails:
                    whitelisted_and_present.append(user_tuple)
                else:
                    added_users.append(user_tuple)

            

            # Determine which whitelisted emails were not found in the file
            removed_emails = all_whitelisted_emails - {email for email, _, _ in emails_in_file}
            removed_users = [(email, '', '') for email in removed_emails]  

            context = {
                'added': added_users,
                'removed': removed_users,
                'file_name': imported_file.name,
                'whitelisted_and_present': whitelisted_and_present
            }
            return HttpResponse(template.render(context, req))

        except Exception as e:
            # In case of any exception, render the template with an error message
            context = {'error': f"An error occurred while processing the file: {str(e)}"}
            return HttpResponse(template.render(context, req))
    else:
        # If it's neither a GET nor a POST with a file, it's an invalid request
        return HttpResponse('Invalid request', status=400)


def add_remove_mentees_from_file(req : HttpRequest):
    list_of_mentees = json.loads(req.body)["list_of_mentees"]
    banana_split = list_of_mentees.split(";")
    added_mentees = banana_split[0].split(",") if len(banana_split) > 0 else []
    removed_mentees = banana_split[1].split(",") if len(banana_split) > 1 else []

    added_list = []
    for mentee_email in added_mentees:
        added_list.append(WhitelistedEmails(str_email=mentee_email))
    print("CUM ",added_list)
    WhitelistedEmails.objects.bulk_create(added_list)
    WhitelistedEmails.objects.filter(str_email__in=removed_mentees).delete()

    return redirect("/available_mentees")


@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')


        exists = User.objects.filter(cls_email_address=email).exists()
        return JsonResponse({'exists': exists})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)