from django.http import HttpResponse, HttpRequest, FileResponse
from django.template import loader, Template
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from utils import development
from datetime import date, datetime, timedelta
from utils.development import print_debug
from utils import security
from .status_codes import bad_request_400
from django.db.models import Count, Q, Value,Case,BooleanField,When,F,OuterRef,Subquery
from .reporting import *

from ..models import User
from ..models import MentorshipRequest
from ..models import Mentor
from ..models import Mentee
from ..models import Interest
from ..models import SystemLogs

from openpyxl import Workbook
from openpyxl.styles import Alignment
from timeit import default_timer as get_runtime
import os
import time


# def default(req: HttpRequest):
#     """
#     Loads the default (root /) page for now until landing page   ##possibly delete this? think isnt being used
#     become the new root route.
#     """
    
#     template: Template = loader.get_template('index.html')
#     context: dict = {}
    
#     return HttpResponse(template.render(context, req)) 

def global_nav_data(req):
    context: dict = {}

    """
    Adding key values to dict for use in the navigation bar.
    """
    authenticated = security.is_logged_in(req.session)
    context['authenticated'] = authenticated

    if authenticated:
        session_user = User.from_session(req.session)
        context['user'] = session_user
        context['org_admin'] = session_user.is_an_org_admin()

    return context

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

@security.Decorators.require_login(bad_request_400)
def dashboard(req):
    start_time = get_runtime()
    template = loader.get_template('dashboard/dashboard.html')
    session_user = User.from_session(req.session).sanitize_black_properties()

    role = session_user.get_database_role_string()
    opposite_role = session_user.get_opposite_database_role_string()

    if session_user.is_super_admin():
        return admin_dashboard(req)
        
    if opposite_role == "Mentor":
        requests = MentorshipRequest.objects.all().filter(mentor_id = OuterRef('pk'),mentee_id=session_user.id)
        requests_count = requests.annotate(c=Count("*")).values('c')

        card_data = User.objects.annotate(
            num_mentees=Count('mentor___mentee_set', distinct=True)
        ).annotate(
            has_maxed_mentees=Case(
                When(num_mentees__gte=F('mentor__int_max_mentees'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).annotate(
                is_requested_by_session=Subquery(requests_count)
                ).filter(
            has_maxed_mentees=False,
              bln_active = True,  # Exclude mentors who have maxed out their mentee slots
        ).filter(
            str_role='Mentor'
        ).select_related(
            'mentor'  # Link each Mentor to the corresponding User account
        ).prefetch_related(
            'interests'  # Prefetch the interests of the associated User
        ).prefetch_related(
            'profile_img_query'
        ).prefetch_related(
            'mentor___mentee_set'
        ).select_related(
                'mentee'
        ).order_by(
                'is_requested_by_session','str_last_name' #make sure all mentors who we can cancel get displayed up top
        ).exclude(
        )
        session_user.has_mentor = session_user.mentee.mentor != None
        session_user.has_maxed_requests_as_mentee = session_user.mentee.has_maxed_request_count()

    if opposite_role == "Mentee":

        #sub query to count the number of requests for setting
        requests = MentorshipRequest.objects.all().filter(mentee_id = OuterRef('pk'),mentor_id=session_user.id)
        requests_count = requests.annotate(c=Count("*")).values('c')

        card_data = User.objects.filter(
            str_role='Mentee',
            bln_active = True,
            mentee__mentor=None
        ).prefetch_related(
            'interests'  # Prefetch the interests of the associated User
        ).prefetch_related(
            'profile_img_query'
        ).prefetch_related(
                'mentee'
        ).prefetch_related(
                'mentor'
        ).prefetch_related(
                'mentee__mentor'
        ).annotate(
                is_requested_by_session=Subquery(requests_count)
        ).order_by(
                'is_requested_by_session','str_last_name' #make sure requested mentees appear first
        )

        session_user.has_mentor = False
        session_user.has_maxed_requests_as_mentee = False
        print(f"finished mentee query as mentor @ {get_runtime()-start_time}")
    
    # Retrieve a list of recommended users
    recommended_users = session_user.get_recomended_users()

    if session_user.is_mentor():
        card_data = card_data.exclude(mentee__mentor__id = session_user.mentor.id)
    elif session_user.is_mentee() and session_user.mentee.mentor:
        card_data = card_data.exclude(mentor__id=session_user.mentee.mentor.id)


    print(f"finished exlusion @ {get_runtime()-start_time}")
    

    interests_with_role_count = Interest.objects.annotate(
                                    mentor_count=Count('user', filter=Q(user__str_role=opposite_role))
                                    ).values('strInterest', 'mentor_count')

    users = [user.sanitize_black_properties() for user in card_data]

    #cache the result of this query so we are not using it in the rendered view
    context = {
                                # Making sure that there are enough users to display
            "recommended_users": recommended_users[0:4] if len(recommended_users) >= 4 else recommended_users[0:len(recommended_users)], 
            "all_users"        : users,
            "interests"        : list(interests_with_role_count),
            "session_user"     : session_user,
            "role"             : role
    }

    
    print("Time for query: ", get_runtime()-start_time)
    render = template.render(context, req)

    print("Time: " ,get_runtime()-start_time)
    return HttpResponse(render)



def admin_dashboard(req):
    """
    TODO JA
    """
    template = loader.get_template('admin_dashboard.html')
    

    overall_stats = get_project_overall_statistics()
    timespan_stats = get_project_time_statistics()

    interests = Interest.objects.all()

    context = {
               "active_mentees"              : overall_stats["active_mentees"              ],
               "assigned_mentees"            : overall_stats["assigned_mentees"            ],
               "unassigned_mentees"          : overall_stats["unassigned_mentees"          ],
               "inactive_mentees"            : overall_stats["inactive_mentees"            ],
               "active_mentors"              : overall_stats["active_mentors"              ],
               "assigned_mentors"            : overall_stats["assigned_mentors"            ],
               "unassigned_mentors"          : overall_stats["unassigned_mentors"          ],
               "inactive_mentors"            : overall_stats["inactive_mentors"            ],
               "mentees_per_mentor"          : overall_stats["mentees_per_mentor"          ],
               "mentor_retention_rate"       : overall_stats["mentor_retention_rate"       ],
              
               "successful_match_rate"       : overall_stats["successful_match_rate"       ],
               "pending_mentors"             : overall_stats["pending_mentors"             ],
              
               "unresolved_reports"          : overall_stats["unresolved_reports"          ],
               
               "interests"                   : interests,
               
               # Daily
               "daily_visitors"                  : timespan_stats["Daily"][0],
               "daily_mentee_signup"             : timespan_stats["Daily"][1],
               "daily_mentor_signup"             : timespan_stats["Daily"][2],
               "daily_assigned_mentees"          : timespan_stats["Daily"][3],
               "daily_deactivate_mentees"        : timespan_stats["Daily"][4],
               "daily_deactivate_mentors"        : timespan_stats["Daily"][5],
               "daily_terminated_mentorships"    : timespan_stats["Daily"][6],

               # Week
               "weekly_visitors"                 : timespan_stats["Weekly"][0],
               "weekly_mentee_signup"            : timespan_stats["Weekly"][1],
               "weekly_mentor_signup"            : timespan_stats["Weekly"][2],
               "weekly_assigned_mentees"         : timespan_stats["Weekly"][3],
               "weekly_deactivate_mentees"       : timespan_stats["Weekly"][4],
               "weekly_deactivate_mentors"       : timespan_stats["Weekly"][5],
               "weekly_terminated_mentorships"   : timespan_stats["Weekly"][6],
               
               # Month
               "monthly_visitors"                : timespan_stats["Monthly"][0],
               "monthly_mentee_signup"           : timespan_stats["Monthly"][1],
               "monthly_mentor_signup"           : timespan_stats["Monthly"][2],
               "monthly_assigned_mentees"        : timespan_stats["Monthly"][3],
               "monthly_deactivate_mentees"      : timespan_stats["Monthly"][4],
               "monthly_deactivate_mentors"      : timespan_stats["Monthly"][5],
               "monthly_terminated_mentorships"  : timespan_stats["Monthly"][6],
               
               # Lifetime
               "lifetime_visitors"               : timespan_stats["Lifetime"][0],
               "lifetime_mentee_signup"          : timespan_stats["Lifetime"][1],
               "lifetime_mentor_signup"          : timespan_stats["Lifetime"][2],
               "lifetime_assigned_mentees"       : timespan_stats["Lifetime"][3],
               "lifetime_deactivate_mentees"     : timespan_stats["Lifetime"][4],
               "lifetime_deactivate_mentors"     : timespan_stats["Lifetime"][5],
               "lifetime_terminated_mentorships" : timespan_stats["Lifetime"][6],
               
            }
    return HttpResponse(template.render(context, req))
