import json
import re
from collections.abc import Callable
from datetime import date
from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import render, redirect
from mentorship_program_app.models import User

from .status_codes import bad_request_400
from utils import security

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

def __validate_request_body(req_callback: Callable, *body_args: str) -> Callable:
    def wrapper(*args):
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
        
        return req_callback(*args)
    
    return wrapper

def validate_request_body(*args: str):
    return lambda func: __validate_request_body(func, *args)

@validate_request_body("fname", "lname", "pronouns", "email", "phone-number", "password")
def register_mentor(req: HttpRequest):
    if req.method == "POST":
        
        incoming_email: str = req.POST["email"]
        
        
        
        if User.objects.filter(clsEmailAddress=req.POST["email"]).count() != 0:    
            return HttpResponse(f"Email {incoming_email} already exsists!")
        
        generated_user_salt = security.generate_salt()
        
        User.objects.create(
            clsEmailAddress = incoming_email,
            strPasswordHash = security.hash_password(req.POST["password"], generated_user_salt),
            strPasswordSalt = generated_user_salt,
            strRole = User.Role.MENTOR_PENDING,
            clsDateJoined = date.today(),
            clsActiveChangedDate = date.today(),
            blnActive = False,
            blnAccountDisabled = False,
            strFirstName = req.POST["fname"],
            strLastName = req.POST["lname"],
            strPhoneNumber = req.POST["phone-number"],
            #clsDateofBirth = clsDateOfBirth,
            #strGender = strGender,
            strPreferredPronouns = req.POST["pronouns"]
        )
        
        return HttpResponse("Registration request successful! We'll get back to ya!")
        
    else:
        return HttpResponse("Bad :(")
    

def view_pending_mentors(req: HttpRequest):
    #TODO Verify youre an admin

    pending_mentors = User.objects.filter(strRole="MentorPending")
    
    out_str = ""
    
    for user in pending_mentors:
        user_info = user.getUserInfo()
        cum = user_info["FirstName"]
        fart = user_info["EmailAddress"]
        out_str += f"Name: {cum}  Email: {fart} id: {user.id} ||"
    
    print(out_str)
    return HttpResponse(str(out_str))


def change_mentor_status(req:HttpRequest):
    #TODO Verify youre an admin
    post_data = json.loads(req.body.decode("utf-8"))

    id = post_data["id"] if "id" in post_data else None
    status = post_data["status"] if "status" in post_data else None
    
    user = User.objects.get(id=id)
    if status == 'Approved':
        user.blnActive = True
        user.strRole = User.Role.MENTOR
    else:
        user.strRole = User.Role.DECLINED
        
    user.save()
        
    return HttpResponse(f"user {id}'s status has been changed to: {status}")
    
    
   
 
def ban_user(req:HttpRequest):
    post_data = json.loads(req.body.decode("utf-8"))
    
    id = post_data["id"] if "id" in post_data else None
    #True or False
    account_disabled = post_data["account_disabled"] if "account_disabled" in post_data else None
    
    user = User.objects.get(id=id)
    
    if(account_disabled):
        user.blnAccountDisabled = True
    else:
        user.blnAccountDisabled = False
    user.save()
    
    return HttpResponse(f"user {id}'s status has been changed to {account_disabled}")

