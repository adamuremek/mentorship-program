"""
/*********************************************************************/
/* FILE NAME: interest_routes.py                                    */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY:   Andrew P                                            */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project supports the mentorship network by enabling the      */
/* management of user interests, which are crucial for matching      */
/* mentors and mentees effectively.                                  */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the server-side logic to handle updates to     */
/* user interests, including additions, deletions, and modifications.*/
/* These operations are restricted to super administrators.          */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: Class for handling HTTP requests                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for parsing JSON data                              */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
import json

from django.http import HttpResponse, HttpRequest
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from .emails import *
from ..models import *

def update_interests(req : HttpRequest):
    """
    Handles POST requests to update user interests. Only accessible by super admins.

    Parameters:
    - req : HttpRequest : The request object containing necessary data.

    Returns:
    - HttpResponse : Response with the result of the update operation.

    This function processes added, deleted, and edited interests based on JSON input from the request body.
    It logs each action in the system logs for auditing purposes.
    """
    if req.method == "POST":
        post_data = json.loads(req.body.decode("utf-8"))
        user_from_session = User.from_session(req.session)
        if not user_from_session.is_super_admin():
            return bad_request_400("Permission denied")
        
        # strings (names)
        add_list = post_data["added"]
        # id's
        delete_list = post_data["deleted"]
        # id's and names
        edit_list = post_data["edited"]

        # Event log
        event_log = []
        print (req.body)
        # add new interests
        added_instances = []
        print ( added_instances)
        for interest in add_list:
            added_instances.append(Interest(strInterest=interest, isDefaultInterest=False))
            
        # Iterate over all the new interests made and retrieve their str and their id for system log
        for interest_object in Interest.objects.bulk_create(added_instances):
            event_log.append(SystemLogs(str_event=SystemLogs.Event.INTERESTS_CREATED_EVENT, str_details=f"{interest_object.id} : {interest_object.strInterest}", specified_user=user_from_session))

        # edit existing interests
        ids_to_edit = [int(interest[0]) for interest in edit_list]
        interests_to_edit = Interest.objects.filter(id__in=ids_to_edit)
        for interest_object in interests_to_edit:
            new_interest = next((interest[1] for interest in edit_list if str(interest_object.id) == interest[0]), None)
            if new_interest is not None:
                old_interest = interest_object.strInterest
                interest_object.strInterest = new_interest
                event_log.append(SystemLogs(str_event=SystemLogs.Event.INTERESTS_UPDATED_EVENT, str_details=f"{interest_object.id} : {old_interest} -> {new_interest}", specified_user=user_from_session))

        Interest.objects.bulk_update(interests_to_edit, ['strInterest'])

        # delete interests
        interests_to_delete = Interest.objects.filter(id__in=delete_list)
        for interest in interests_to_delete:
            event_log.append(SystemLogs(str_event=SystemLogs.Event.INTERESTS_DELETED_EVENT, str_details=f"{interest.id} : {interest.strInterest}", specified_user=user_from_session))
        interests_to_delete.delete()

        SystemLogs.objects.bulk_create(event_log)
        
        return HttpResponse("Updated")
    return HttpResponse("Needs to be POST")
