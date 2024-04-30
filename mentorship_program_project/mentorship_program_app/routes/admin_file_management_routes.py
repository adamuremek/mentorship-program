"""
/*********************************************************************/
/* FILE NAME: admin_file_management_routes.py                                  */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew P, Adam U                                      */
/* (OFFICIAL) DATE CREATED: Long ago                                 */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is designed to enhance the connectivity and          */
/* management of SVSU CSIS students and their mentors. This includes */
/* dynamically managing mentee access and roles within the platform. */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains functions for managing mentee roles within the */
/* platform, such as adding or removing mentees from a whitelist     */
/* based on the administrative input through file uploads.           */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: Class for handling HTTP requests                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for parsing JSON data                              */
/* - loader: Module to load Django templates                         */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

import json
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import  redirect
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from .emails import *
from ..models import *

def add_remove_mentees_from_file(req : HttpRequest):
    '''
    Description
    -----------
    Function to add and remove mentee emails from a whitelist based on a provided list within a single HttpRequest. The request contains a string of mentee emails to be added or removed, formatted and separated by specific delimiters. Emails to be added are separated from those to be removed by a semicolon (";"), and individual emails within those groups are separated by commas (",").

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object carrying the payload with the list of mentees' emails.

    Returns
    -------
    HttpResponseRedirect
        Redirects to the "/available_mentees" URL after processing the list.

    Authors
    -------
    - Andrew P
    - Adam U.
    '''
    list_of_mentees = json.loads(req.body)["list_of_mentees"]
    banana_split = list_of_mentees.split(";")
    added_mentees = banana_split[0].split(",") if len(banana_split) > 0 else []
    removed_mentees = banana_split[1].split(",") if len(banana_split) > 1 else []
    # Reactivate users by setting bln_account_disabled to False
    reactivate_users = User.objects.filter(cls_email_address__in=added_mentees)

    # Loop through the queryset and update each user object
    for user in reactivate_users:
        print(user.cls_email_address)
        user.bln_account_disabled = False
        user.save()



    added_list = []
    for mentee_email in added_mentees:
        added_list.append(WhitelistedEmails(str_email=mentee_email))
        
    WhitelistedEmails.objects.bulk_create(added_list)
    WhitelistedEmails.objects.filter(str_email__in=removed_mentees).delete()

    return redirect("/available_mentees")

def process_file(req: HttpRequest):
    '''
    Description
    -----------
    Function to process an uploaded file containing email addresses, first names, and last names separated by tabs. It identifies emails that are both whitelisted and present in the file, emails in the file not whitelisted (considered as 'added users'), and whitelisted emails not found in the file (considered as 'removed users'). The function renders a template displaying these categorized emails and additional information.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object, which can carry the uploaded file in a POST request or handle a GET request to initially render the form.

    Returns
    -------
    HttpResponse
        Renders an HTML template with context data that includes lists of added, removed, and already whitelisted users found in the uploaded file, along with the file name and any error messages.

    Authors
    -------
    - Andrew P
    '''
    user = User.from_session(req.session)
    if not user.is_super_admin():
        return bad_request_400("permission denied!")

    template = loader.get_template('admin/available_mentees.html')
    
    # its a get request the first time you load the page
    if req.method == "GET":
        context = {'added': [], 'removed': [], 'file_name': ''}
        return HttpResponse(template.render(context, req))
    # after you upload a file, it'll be a post request and all the fun stuff gets to happen
    if req.method == 'POST' and 'fileUpload' in req.FILES:
        imported_file = req.FILES['fileUpload']
        # users whos accounts are still valid
        whitelisted_and_present = []
        # users to be added
        added_users = []
        # all the emails that exist already
        all_whitelisted_emails = set(WhitelistedEmails.objects.values_list('str_email', flat=True))
        # set of all the emails and names in the file
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
                # we kinda ignore these
                if email in all_whitelisted_emails:
                    whitelisted_and_present.append(user_tuple)
                # these users could be added if admin chooses
                else:
                    added_users.append(user_tuple)  

            

            # Determine which whitelisted emails were not found in the file
            # the admin can chose to remove these users
            removed_emails = all_whitelisted_emails - {email for email, _, _ in emails_in_file}
            removed_users = [(email, '', '') for email in removed_emails]  
            user_to_deactivate = User.objects.filter(cls_email_address__in=removed_emails)
            for user in user_to_deactivate:
                User.disable_user(user, "User was disabled from file upload")
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
    
def available_mentees(req: HttpRequest):
    user = User.from_session(req.session)
    if not user.is_super_admin():
        return bad_request_400("permission denied!")
    '''
    Loads the page for the admin to upload a file to add/remove mentees who are eligible

    - Andrew P
    '''
    template = loader.get_template('admin/available_mentees.html')
    context = {}
    return HttpResponse(template.render(context,req))