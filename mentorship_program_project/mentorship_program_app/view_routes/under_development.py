import json
import re
from collections.abc import Callable
from datetime import date

from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from utils.development import print_debug

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
            #organization.save()
        else:
            organization = Organization.objects.get(str_org_name=req.POST["organization"])
            
        pending_mentor_object.account.cls_email_address = incoming_email
        pending_mentor_object.account.str_first_name = req.POST["fname"]
        pending_mentor_object.account.str_last_name = req.POST["lname"]
        pending_mentor_object.account.str_phone_number = req.POST["phone"]

        #were not getting the data from the incoming form
        #if this is a thing we need to keep track of we should prolly send it
        #idk tho do whatevs -dk
        #cls_date_of_birth = cls_date_of_birth 
        #str_gender = str_gender,


        str_preferred_pronouns = req.POST["pronouns"]
        mentor = User.objects.get(cls_email_address = incoming_email)
        
        pending_mentor_object.str_job_title =  req.POST["jobTitle"]
        pending_mentor_object.str_experience = req.POST["experience"]
        pending_mentor_object.organization.add(organization)

        parsed_user_interests = [
                                    Interest.get_or_create_interest(interest) 
                                    for interest in req.POST["interests"].split(",")[0:-1]
                                 ]


        pending_mentor_object.account.save()
        pending_mentor_object.save()

        for interest in parsed_user_interests:
            pending_mentor_object.account.interests.add(interest)


        pending_mentor_object.save()
            
            
        
        return HttpResponse("Registration request successful! We'll get back to ya!")
        
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

    # get all mentors who are still pending
    pending_mentors = User.objects.filter(str_role="MentorPending")
    
    out_str = ""
    
    for user in pending_mentors:
        user_info = user.get_user_info()
        first_name = user_info["FirstName"]
        last_name = user_info["LastName"]
        email = user_info["EmailAddress"]
        out_str += f"Name: {first_name} {last_name} Email: {email} id: {user.id} ||"

    return HttpResponse(str(out_str))


def change_mentor_status(req:HttpRequest):
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
    "user {id}'s status has been changed to: {status}"
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    '''
    #TODO Verify you're an admin

    # Extract mentor ID and status from request data
    post_data = json.loads(req.body.decode("utf-8"))
    id = post_data["id"] if "id" in post_data else None
    status = post_data["status"] if "status" in post_data else None
    
    # Retrieve user object based on ID
    user = User.objects.get(id=id)
    
    # Update user role and activation status based on provided status
    if status == 'Approved':
        user.bln_active = True
        user.str_role = User.Role.MENTOR
    else:
        user.str_role = User.Role.DECLINED
        
    # Save changes to user object
    user.save()
        
    return HttpResponse(f"user {id}'s status has been changed to: {status}")


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
        #we should never get here, but just in case for some reason
        return bad_request_400("internal error occured")

    mentorship_request = MentorshipRequest.create_request(mentor_account.id,mentee_account.id)
    if mentorship_request: 
        mentorship_request.save() 
    else:
        print("this request already exists, IDENTITY CRISIS ERROR 🤿  ⛰️")

    ##print_debug(user.has_requested_user(mentor_id))
    return HttpResponse(json.dumps({"result":"created request!"}));


@security.Decorators.require_login(bad_request_400)
def update_profile_img(req: HttpRequest)->HttpResponse:
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

    # Get the user id from the current session
    user = User.from_session(req.session)
    int_user_id = user.id
    #   Get the name of the file through an HTTP POST request with JSON data.
    post_data = json.loads(req.body.decode("utf-8"))
    str_img_name = post_data["image"] if "image" in post_data else None
    
    #   If the name of the file is not valid (wrong file extension or insufficient name length),
    #   return an HttpResponse saying the user's profile was not modified.
    if str_img_name == None:
        return HttpResponse(f"User {int_user_id}'s image profile was NOT modified")
    elif len(str_img_name) < 5:
        return HttpResponse(f"File name was invalid. User {int_user_id}'s profile was NOT modified.")
    elif str_img_name.endswith(".png") == False:
        return HttpResponse(f"File name was invalid. User {int_user_id}'s profile was NOT modified.")
    elif str_img_name.endswith(".jpg") == False:
        return HttpResponse(f"File name was invalid. User {int_user_id}'s profile was NOT modified.")
    
    #   Otherwise, continue on with running the function.
    else:
        #   Check if a 'ProfileImg' instance exists that is associated
        #   with the user currently logged into the system.
        profile_img = ProfileImg.objects.get(user=user)
        if profile_img == None:
            #   If not, create a new instance of the ProfileImg model 
            #   and store it in the program's database
            bool_flag = ProfileImg.create_from_user_id(int_user_id, str_img_name)
            #   Return a response saying the process did not go through, if so.
            if bool_flag == False:
                return HttpResponse(f"Something went wrong while trying to modify user {int_user_id}'s profile.")
            #   If the process did go through, get the newly created instance.
            profile_img = ProfileImg.objects.get(user=user)
        else:
            #   Otherwise, store the image name and save the image instance
            profile_img.img_title = str_img_name

        #   Take the name of the image file and store it in the user's ImageView.
        profile_img.img_profile = str_img_name
        profile_img.save()

        return HttpResponse(f"User {int_user_id}'s image profile was SUCCESSFULLY modified")


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
    """

    #Grab the users current session
    user = User.from_session(req.session)
    str_title = req.POST.get("title", None)
    str_body = req.POST.get("body", None) 
    bool_flag = False

    #Check if the title and body are None
    if str_title != None and str_body != None:
        #create the note and save it to the database.
        bool_flag = Notes.create_note(user.id, str_title, str_body)
    else:
        return bad_request_400("Invalid title or body")

    #Check if the note was created.
    if bool_flag:
        return HttpResponse("Note created!")
    else:
        return HttpResponse("Note creation failed")

    



