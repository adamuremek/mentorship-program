from django.http import HttpResponse, HttpRequest, FileResponse
from django.template import loader, Template
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from utils import development
from datetime import date, datetime, timedelta
from utils.development import print_debug
from utils import security
from .status_codes import bad_request_400
from django.db.models import Count, Q, Value,Case,BooleanField,When,F
from .reporting import *

from ..models import User
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

    return context

def landing(req):
    """
    Renders the landing page for the application.

    Now redirects to dashboard if logged in - Tanner
    """
    if security.is_logged_in(req.session): 
        return redirect("/dashboard")

    template: Template = loader.get_template('landing_page.html')
    context: dict = {}
    
    return HttpResponse(template.render(context, req))

@security.Decorators.require_login(bad_request_400)
def dashboard(req):
    start_time = get_runtime()
    template = loader.get_template('dashboard/dashboard.html')
    session_user = User.from_session(req.session).sanitize_black_properties()

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


    if session_user.is_super_admin():
        return admin_dashboard(req)

        

    if opposite_role == "Mentor":
        card_data = User.objects.annotate(
        num_mentees=Count('mentor___mentee_set', distinct=True)
        ).annotate(
            has_maxed_mentees=Case(
                When(num_mentees__gte=F('mentor__int_max_mentees'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).filter(
            has_maxed_mentees=False,  # Exclude mentors who have maxed out their mentee slots
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
        )

        users = [user.sanitize_black_properties() for user in card_data]
        session_user.has_maxed_requests_as_mentee = session_user.mentee.has_maxed_request_count()



    if opposite_role == "Mentee":
        
        card_data = User.objects.filter(
            str_role='Mentee',
            mentee__mentor=None
        ).prefetch_related(
            'interests'  # Prefetch the interests of the associated User
        ).prefetch_related(
            'profile_img_query'
        )

        #card_data = User.objects.filter(str_role=opposite_role). \
        #prefetch_related('interests'). \
        #prefetch_related('profile_img_query'). \
        #defer(
        #    "cls_email_address",
        #    "str_password_hash",
        #    "str_password_salt",
        #    "str_role",
        #    "cls_date_joined",
        #    "cls_active_changed_date",
        #    "bln_active",
        #    "bln_account_disabled",
        #    "str_phone_number",
        #    "str_last_login_date",
        #    "str_gender",
        #    "str_preferred_pronouns",
        #    "str_bio",
        #)
        users = [user.sanitize_black_properties() for user in card_data]
    
    #print("starting recomendation algorithm")
    #recommended_users = session_user.get_recomended_users()
    #print("ending recomendation algorithm")
    #for p in recommended_users:
    #    print((p.str_first_name,p.str_last_name,p.likeness))

    recommended = session_user.get_recomended_users()

    #filter out existing mentor relationships on the dashboard
    if session_user.is_mentor():
        card_data = card_data.exclude(mentee__mentor = session_user.mentor)
    elif session_user.is_mentee() and session_user.mentee.mentor:
        card_data = card_data.exclude(id=session_user.mentee.mentor.account.id)
    

    interests_with_role_count = Interest.objects.annotate(
                                    mentor_count=Count('user', filter=Q(user__str_role=opposite_role))
                                    ).values('strInterest', 'mentor_count')

    # Modified the code here so to not call 3 foreach loops lmk if this breaks anything -JA 
    #set up the django users to include a property indicateing they have been reqeusted by the current user

    for user in users:
        user.is_requested_by_session = False

    #cache the result of this query so we are not using it in the rendered view
    context = {
                                # Making sure that there are enough users to display
            "recommended_users": recommended[0:4] if len(recommended) >= 4 else recommended[0:len(recommended)], 
            "all_users"        : users if len(users) >= 4 else [],
            "interests"        : list(interests_with_role_count),
            "session_user"     : session_user,
            "role"             : role
    }

    
    print("Time for query: ", get_runtime()-start_time )
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
               "mentor_turnover_rate"        : overall_stats["mentor_turnover_rate"        ],
               "total_approved_mentorships"  : overall_stats["total_approved_mentorships"  ],
               "total_requested_mentorships" : overall_stats["total_requested_mentorships" ],
               "successful_match_rate"       : overall_stats["successful_match_rate"       ],
               "pending_mentors"             : overall_stats["pending_mentors"             ],
               "total_terminated_mentorships": overall_stats["total_terminated_mentorships"],
               "mentees_reported"            : overall_stats["mentees_reported"            ],
               "unresolved_reports"          : overall_stats["unresolved_reports"          ],
               
               # Daily
               "daily_visitors"              : timespan_stats["Daily"][0],
               "daily_mentee_signup"         : timespan_stats["Daily"][1],
               "daily_mentor_signup"         : timespan_stats["Daily"][2],
               "daily_assigned_mentees"      : timespan_stats["Daily"][3],
               "daily_deactivate_mentees"    : timespan_stats["Daily"][4],
               "daily_deactivate_mentors"    : timespan_stats["Daily"][5],

               # Week
               "weekly_visitors"             : timespan_stats["Weekly"][0],
               "weekly_mentee_signup"        : timespan_stats["Weekly"][1],
               "weekly_mentor_signup"        : timespan_stats["Weekly"][2],
               "weekly_assigned_mentees"     : timespan_stats["Weekly"][3],
               "weekly_deactivate_mentees"   : timespan_stats["Weekly"][4],
               "weekly_deactivate_mentors"   : timespan_stats["Weekly"][5],
               
               # Month
               "monthly_visitors"             : timespan_stats["Monthly"][0],
               "monthly_mentee_signup"        : timespan_stats["Monthly"][1],
               "monthly_mentor_signup"        : timespan_stats["Monthly"][2],
               "monthly_assigned_mentees"     : timespan_stats["Monthly"][3],
               "monthly_deactivate_mentees"   : timespan_stats["Monthly"][4],
               "monthly_deactivate_mentors"   : timespan_stats["Monthly"][5],
               
               # Lifetime
               "lifetime_visitors"            : timespan_stats["Lifetime"][0],
               "lifetime_mentee_signup"       : timespan_stats["Lifetime"][1],
               "lifetime_mentor_signup"       : timespan_stats["Lifetime"][2],
               "lifetime_assigned_mentees"    : timespan_stats["Lifetime"][3],
               "lifetime_deactivate_mentees"  : timespan_stats["Lifetime"][4],
               "lifetime_deactivate_mentors"  : timespan_stats["Lifetime"][5],
               
            }
    return HttpResponse(template.render(context, req))
