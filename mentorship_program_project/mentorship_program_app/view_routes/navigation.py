import json
from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from utils import development
from datetime import datetime, timedelta
from utils.development import print_debug
from utils import security
from .status_codes import bad_request_400
from django.db.models import Count, Q

from ..models import User
from ..models import Mentor
from ..models import Mentee
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

@security.Decorators.require_login(bad_request_400)
def dashboard(req):
    template = loader.get_template('dashboard/dashboard.html')
    session_user = User.from_session(req.session)
   
    # get the users of the opposite role to be displayed
    # mentors see mentees and mentees see mentors


    ## changing to use functions to ping data base for approval VVVVVV
    ##opposite_role = 'Mentee' if role == 'Mentor' else 'Mentor'

    ## New method vvvv From tanner/david
    
    # TODO: 
    # now that were passing session_user data to the view,
    # we might want to concider re-writing the dashboard template
    # to use the session_user object instead of passing in an extra role
    # string in the context for cleanlyness
    # plus the is_mentor / is_mentee functions ping the database to ensure the 
    # existence of a mentor or mentee data acount respectivly, so there fore cannot 
    # be decyned unlike the str_role which could potnentially store diffeering state from the db
    # minor nitpic at best, but if people want to get it swapped over or don't mind me
    # messing with their code we could put it in
    role = session_user.get_database_role_string()
    opposite_role = session_user.get_opposite_database_role_string()

    card_data = User.objects.filter(str_role=opposite_role)

    print(card_data)

    # Using the Interest's many-to-many relation with the User table
    # Count all the interests for the opposing role
    interests_with_role_count = Interest.objects.annotate(mentor_count=Count('user', filter=Q(user__str_role=opposite_role))).values('strInterest', 'mentor_count')

    #set up the django users to include a property indicateing they have been reqeusted by the current user
    users = [users.sanitize_black_properties() for users in card_data] 
    for u in users:
        u.is_requested_by_session = u.has_requested_user(session_user.id)
    
    context = {
            "recommended_users": [users.sanitize_black_properties() for users in card_data[0:4]],
            "all_users"        : users,
            "interests"        : list(interests_with_role_count),
            "session_user"     : session_user.sanitize_black_properties(),
            "role"             : role
    }

    return HttpResponse(template.render(context, req))

def admin_dashboard(req):
    template = loader.get_template('admin_dashboard.html')
    inactive_date = datetime.now() - timedelta(days=365)
    
    # Query to count the number of Mentees who are currently inactive
    inactive_mentees_count = User.objects.filter(str_role='Mentee', str_last_login_date__lt=inactive_date).count()
    # Query to count the number of Mentees who are currently active
    active_mentees_count = User.objects.filter(str_role='Mentee', str_last_login_date__gte=inactive_date).count()
    # Query to count the number of Mentors who are currently inactive
    inactive_mentors_count = User.objects.filter(str_role='Mentor', str_last_login_date__lt=inactive_date).count()
    # Query to count the number of Mentors who are currently active
    active_mentors_count = User.objects.filter(str_role='Mentor',str_last_login_date__gte=inactive_date).count()
    # Number of total mentees
    total_mentees = User.objects.filter(str_role='Mentee').count()
    # Number of total mentors
    total_mentors = User.objects.filter(str_role='Mentor').count()

    # number of pending mentors
    pending_mentor_count = User.objects.filter(str_role='MentorPending').count()
    context = {"pending_mentor_count": pending_mentor_count,
               "active_mentees_count" : active_mentees_count,
               "inactive_mentees_count" : inactive_mentees_count,
               "active_mentors_count" : active_mentors_count,
               "inactive_mentors_count" : inactive_mentors_count,
               "mentees_per_mentor" : round(total_mentees/total_mentors,2),
               "mentor_turnover_rate" : round((inactive_mentors_count / total_mentors) * 100),
               "mentor_retention_rate" : round(100- ((inactive_mentors_count / total_mentors) * 100))
               
               }
    return HttpResponse(template.render(context, req))
