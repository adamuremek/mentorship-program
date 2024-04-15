"""
/*********************************************************************/
/* FILE NAME: landing_routes.py                                        */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: a bunch of people                                     */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to provide a comprehensive platform for         */
/* mentorship within the educational sector, facilitating            */
/* meaningful connections between students and industry professionals*/
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file handles the rendering and redirection logic for the     */
/* application's landing page, based on user authentication status.  */
/* It serves as the first interaction point for users with the       */
/* mentorship platform, directing them appropriately.                */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - loader: Module to load Django templates                         */
/* - redirect: Function to redirect the user to a different URL      */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/*********************************************************************/
"""

from django.http import HttpResponse
from django.template import loader, Template
from django.shortcuts import  redirect
from mentorship_program_app.models import *
from utils import security
from ..models import *

def landing(req):
    """
    Renders the landing page for the application.

    Now redirects to dashboard if logged in - Tanner
    """
    if security.is_logged_in(req.session): 
        u = User.from_session(req.session)
        if u.is_mentee() and u.mentee.mentor:
            return redirect(f"/universal_profile/{u.mentee.mentor.account.id}")
        return redirect("/dashboard")

    template: Template = loader.get_template('landing_page.html')
    context: dict = {}
    
    return HttpResponse(template.render(context, req))

# Pho Post handler for landing-page login card
def landingPost(req):
    if req.method == 'POST':
        return redirect('dashboard')
    else:
        return redirect('landing')