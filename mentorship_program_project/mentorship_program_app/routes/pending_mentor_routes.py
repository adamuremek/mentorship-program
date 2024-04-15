"""
/*********************************************************************/
/* FILE NAME: pending_mentor_routes.py                               */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew, Adam U, Jordan                                */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate the administration of mentorship  */
/* within the platform, particularly focusing on the management and  */
/* oversight of mentors by administrators. This includes viewing,    */
/* approving, and rejecting mentor applications, as well as managing */
/* mentor profiles and statuses.                                     */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the functions necessary for administrators to  */
/* view and manage mentor details and statuses. It includes          */
/* functionalities to view pending mentors, approve or reject mentor */
/* statuses, and change mentor details.                              */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - loader: Utility for loading HTML templates                      */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import  redirect
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from .emails import *
from ..models import *

@security.Decorators.require_login(bad_request_400)
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
        phone = user.cls_email_address
        email = user.str_phone_number
        
        user_interests = []
        for interest in interests:
            user_interests.append(interest.strInterest)



        context = {"first_name": user.str_first_name,
                   "last_name": user.str_last_name,
                   "job_title": mentor.str_job_title,
                   "organization": organization,
                   "user_interests": user_interests,
                   "experience" : mentor.str_experience,
                   "phone" : phone,
                   "email" : email,
                   "user" : user.sanitize_black_properties(),
                   }
        return HttpResponse(template.render(context, req))

  
    return HttpResponse("eat my fat nuts!")

@security.Decorators.require_login(bad_request_400)
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
    session_user = User.from_session(req.session)
    if (not session_user.is_super_admin()):
        return bad_request_400("permission denied!")

    if req.method == "POST":
        HttpResponse("wtf")

    # Extract mentor ID and status from request data
    mentor_id = req.POST["mentor_id"]
    status = req.POST["status"]
    
    # Retrieve user object based on ID
    mentor_object = User.objects.get(id=mentor_id)
    
    # Update user role and activation status based on provided status                                           
    if status == 'Approved':
        mentor_object.bln_active = True
        mentor_object.str_role = User.Role.MENTOR
        mentor_object.save()
        mentor_accepted_email(mentor_object.cls_email_address)  
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_APPROVED_EVENT, specified_user=mentor_object, str_details=f"Handled by: {session_user.id}")
    else:
        mentor_denied_email(mentor_object.cls_email_address)
        #TODO change the mentor object to be deactivated if its deleted the system log for that user is also deleted
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_DENIED_EVENT, specified_user=mentor_object, str_details=f"Handled by: {session_user.id}")
        mentor_object.delete()

    # Save changes to user object

    # Redirect back to the view_pending page
    return redirect("/view_pending")


@security.Decorators.require_login(bad_request_400)
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
    session_user = User.from_session(req.session)
    is_super_admin = session_user.is_super_admin()

    if not(is_super_admin):
        return redirect("/")

    template = loader.get_template('pending_mentors.html')
    # Get all mentors who are still pending
    pending_mentors = User.objects.filter(str_role="MentorPending")
    
    context = {"pending_mentors" : pending_mentors}
    
    return HttpResponse(template.render(context, req))
