import json
from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from utils import development
from utils.development import print_debug
from utils import security
from .status_codes import invalid_request_401
from django.db.models import Count, Q

from ..models import User
from ..models import Interest



def default(req: HttpRequest):
    """
    Loads the default (root /) page for now until landing page 
    become the new root route.
    """
    
    template: Template = loader.get_template('index.html')
    context: dict = {}
    
    return HttpResponse(template.render(context, req)) 

def landing(req):
    """
    Renders the landing page for the application.
    """
    
    template: Template = loader.get_template('landing_page.html')
    context: dict = {}
    
    return HttpResponse(template.render(context, req))

@security.Decorators.require_login(invalid_request_401)
def dashboard(req):
    template = loader.get_template('dashboard/dashboard.html')

    role = User.objects.get(id=req.session["user_id"]).strRole
    # get the users of the opposite role to be displayed
    # mentors see mentees and mentees see mentors
    opposite_role = 'Mentee' if role == 'Mentor' else 'Mentor'
    card_data = User.objects.filter(strRole=opposite_role)

    # Using the Interest's many-to-many relation with the User table
    # Count all the interests for the opposing role
    interests_with_role_count = Interest.objects.annotate(mentor_count=Count('user', filter=Q(user__strRole=opposite_role))).values('strInterest', 'mentor_count')
    
    context = {
            "recommended_users": [users.sanitize_black_properties() for users in card_data[0:4]],
            "all_users"        : [users.sanitize_black_properties() for users in card_data],
            "role"             : role,
            "interests"        : list(interests_with_role_count)
    }

    return HttpResponse(template.render(context, req))

def admin_dashboard(req):
    context = {}
    return HttpResponse(template.render(context, req))