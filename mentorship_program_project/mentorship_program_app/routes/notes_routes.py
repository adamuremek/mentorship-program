"""
/*********************************************************************/
/* FILE NAME: note_routes.py                                         */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Adam and Justin                                       */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate secure and efficient management   */
/* of user notes within the mentorship platform, allowing users to   */
/* create, update, and delete personal notes.                        */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the logic for managing user notes, including   */
/* creating, updating, and removing notes. It ensures users can      */
/* manage their personal notes effectively, with functionalities     */
/* supported through web-based requests.                             */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - json: Module for parsing JSON data                              */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""
import json
from django.http import  HttpRequest
from django.shortcuts import redirect
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from .emails import *
from ..models import *

@security.Decorators.require_login(bad_request_400)
def create_note(req : HttpRequest):
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