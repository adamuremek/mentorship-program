"""
/*********************************************************************/
/* FILE NAME: faq_routes.py                                                 */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY:                                                       */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This file is part of an educational initiative to foster          */
/* connections between students and professionals in the CSIS field  */
/* at SVSU. The project facilitates mentorships by providing an      */
/* interactive platform for learning and guidance.                   */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file handles the display of the Frequently Asked Questions   */
/* (FAQ) page on the platform. It serves as a resource for users to  */
/* obtain quick answers to common questions about the mentorship     */
/* program.                                                          */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - loader: Module to load Django templates                         */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

from django.http import HttpResponse
from django.template import loader
from mentorship_program_app.models import *
from ..models import *

def faq(req):
    template = loader.get_template('faq.html')
    context = {}
    return HttpResponse(template.render(context, req))