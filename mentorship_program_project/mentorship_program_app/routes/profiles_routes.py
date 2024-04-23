"""
/********************************************************************************/
/* FILE NAME: profile_routes.py                                                 */
/********************************************************************************/
/* PART OF PROJECT: Mentorship Program                                          */
/********************************************************************************/
/* WRITTEN BY: Andrew, Jordan, Adam and Logan                                   */
/* DATE CREATED:                                                                */
/********************************************************************************/
/* PROJECT PURPOSE:                                                             */
/*                                                                              */
/* This project aims to facilitate the administration and personalization       */
/* of user profiles within the mentorship platform, focusing on profile         */
/* image updates, personal details adjustments, and overall profile management. */
/********************************************************************************/
/* FILE PURPOSE:                                                                */
/*                                                                              */
/* This file contains the functions necessary for users and administrators      */
/* to manage and personalize profiles, including updating profile images,       */
/* editing personal details, and viewing detailed profile information.          */
/********************************************************************           */
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                              */
/*                                                                              */
/* - HttpRequest: For obtaining details of HTTP requests                        */
/* - HttpResponse: Class for sending HTTP responses                             */
/* - loader: Utility for loading HTML templates                                 */
/* - redirect: Function to redirect the user to a different URL                 */
/* - ObjectDoesNotExist: Exception for handling non-existent objects            */
/********************************************************************************/
/* MODIFICATION HISTORY:                                                        */
/********************************************************************************/
/* Date       | Changed By | Changes Made                                       */
/********************************************************************************/
"""
import json
import os
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import  redirect
from django.core.exceptions import ObjectDoesNotExist
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from mentorship_program_project.settings import BASE_DIR, MEDIA_ROOT
from .emails import *
from ..models import *


from typing import Dict
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
def universalProfile(req : HttpRequest, user_id : int):
    '''
    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object.
    - user_id : int
        The unique identifier of the user whose profile is to be displayed.

    Returns
    -------
    HttpResponse
        Renders and returns the universal profile page with context data including the user's details, interests, mentorship requests, and notes.

    Raises
    ------
    - ObjectDoesNotExist
        If no User object with the given `user_id` exists.

    Example Usage
    -------------
    universalProfile(request, 42)
    Displays the profile page for the user with id=42.

    Authors
    -------
    - Andrew P
    - Logan Z
    - Adam U
    - Jordan A
'''
   
    profile_page_owner = None
    # Attempt to retrieve the profile page owner from the database
    try:
        profile_page_owner = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return bad_request_400("user page does not exist")

    # if the users account is disabled, you can't view their profile
    if not profile_page_owner.bln_active:
        return bad_request_400("user page does not exist")

    # Load the template for the profile page
    template = loader.get_template('group_view/combined_views.html')
    signed_in_user = User.from_session(req.session)
    signed_in_user = User.from_session(req.session)

    signed_in_user.has_requested_this_user = signed_in_user.has_requested_user(profile_page_owner)
  
    
    # the user object for the page owner
    page_owner_user = User.objects.get(id=user_id)
    # Determine the role-based object for the page owner (mentee or mentor)
    page_owner_go_fuck_yourself = getattr(page_owner_user, 'mentee' if page_owner_user.is_mentee else 'mentor', None)
    # Fetch interests linked to the user
    interests = page_owner_user.interests.filter(user=page_owner_user)
    is_page_owner = signed_in_user == page_owner_user
    # Compile a list of user interests for the template context
    user_interests = []
    for interest in interests:
        user_interests.append(interest)

    # Declare phone number info incase of mentor
    user_phone_number = ""
    user_country_code = ""

    # all interests (used for editing profile)
    all_interests = Interest.objects.all()
    pendingList = []
    notes = None
    max_mentees = None
    num_mentees = None
    
    # Added this for debug
    mentees_or_mentor = []
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
        
        user_phone_full = profile_page_owner.str_phone_number
        
        if user_phone_full != None and user_phone_full.strip() != "":
            user_phone_full = user_phone_full.split(" ")
            user_country_code = user_phone_full[0]
            user_phone_number = " ".join(user_phone_full[1:])

    user_pronouns = page_owner_user.str_preferred_pronouns
    if user_pronouns != None:
        user_pronouns = user_pronouns.split("/") if user_pronouns != "/" else ["",""]
    else:
        # this is the most bullshit line of code ive ever written
        # it works tho <:D
        # This application is flawless as far as im concerned
        # im glad lol, truly a masterpiece

        # Best code we've ever written
        #                - 2 senior developers
        user_pronouns = ["",""]

    # Ensure that the profile picture exist
    # If not use the default profile picture
    page_owner_profile_url = page_owner_user.profile_img.img.url
    if not os.path.exists(str(settings.MEDIA_ROOT) + page_owner_profile_url.replace("/media", "")):
        page_owner_profile_url = "/media/images/default_profile_picture.png"
        
    country_codes : Dict
    with open('mentorship_program_app/routes/countries.json', 'r') as file:
        country_codes = json.load(file)
        country_codes = sorted(country_codes, key=lambda item: item["dial_code"])

    context = {
                "signed_in_user": signed_in_user.sanitize_black_properties(),
                "is_page_owner": is_page_owner,
                "page_owner_user":page_owner_user,
                "page_owner_profile_url":page_owner_profile_url,
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
                'experiencelist': ['0-4 years','5-9 years', '10+ years'],
                'pronounlist1': ['', 'he', 'she', 'they'],
                'pronounlist2': ['', 'him', 'her', 'them'],
                'pronoun1': user_pronouns[0],
                'pronoun2': user_pronouns[1],
                'country_codes' : country_codes,
                'user_country_code' : user_country_code,
                'user_phone_number' : user_phone_number,
                "is_admin": signed_in_user.is_super_admin()
               }
    return HttpResponse(template.render(context,req)) # Hi :D


def save_profile_info(req : HttpRequest, user_id : int):
    """
    Description
    ===========
    
    This route applies profile edits sent in the request to the respective proifle.

    Author
    ======
    Adam U. ( ͡° ͜ʖ ͡°) 

    Modification History
    ====================
    Justin Goupil - Fix for orphaned profile images when a user replaced their profile image with another. 
    """

    if req.method == "POST":
        #Get the user being modified
        page_owner_user = User.objects.get(id=user_id)
        if page_owner_user.is_mentor():
            if "select-experience" in req.POST:
                page_owner_user.mentor.str_experience = req.POST["select-experience"]
            if "job-title-input" in req.POST:
                page_owner_user.mentor.str_job_title = req.POST["job-title-input"]

        if "firstname-edit" in req.POST:
            page_owner_user.str_first_name = req.POST["firstname-edit"]
        
        if "lastname-edit" in req.POST:
            page_owner_user.str_last_name = req.POST["lastname-edit"]
        #Change profile picture
        if "profile_image" in req.FILES:
            new_pfp = req.FILES["profile_image"]

            # update_profile_img(user_id, new_pfp)

            old_profile_image = f'{MEDIA_ROOT}{page_owner_user.profile_img.img.url}'
            default_profile_image = f"{MEDIA_ROOT}images/default_profile_picture.png"
            
            if old_profile_image != default_profile_image and os.path.exists(old_profile_image):
                print("profile pic has been deleted")
                os.remove(old_profile_image)
            
            page_owner_user.profile_img.img.save(new_pfp.name, new_pfp)


        #Change prefered pronouns
        
        if "pronouns1" in req.POST or "pronouns2" in req.POST:
            page_owner_user.str_preferred_pronouns = f"{req.POST['pronouns1']}/{req.POST['pronouns2']}" 

        if "phone-country-code" in req.POST or "phone-edit" in req.POST:
            page_owner_user.str_phone_number = f"{req.POST['phone-country-code']} {req.POST['phone-edit']}"
            pass

        #Set the new interests
        new_interests: list = req.POST.getlist("selected_interests")
        interest_data = Interest.objects.filter(strInterest__in=new_interests)

        page_owner_user.interests.clear()
        page_owner_user.interests.add(*interest_data)

        # Set Max Mentees
        if page_owner_user.is_mentor():
            if req.POST["max_mentees"]:
                page_owner_user.mentor.int_max_mentees = req.POST["max_mentees"]
            page_owner_user.mentor.save()

        #Set the new bio
        page_owner_user.str_bio = req.POST["bio"]
        page_owner_user.save()
        

    return redirect(f"/universal_profile/{user_id}")