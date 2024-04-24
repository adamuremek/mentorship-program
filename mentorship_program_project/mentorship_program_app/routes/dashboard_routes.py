"""
/*********************************************************************/
/* FILE NAME: dashboard_routes.py                                           */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: A lot of people at different times                    */
/* (OFFICIAL) DATE CREATED: Long ago                                 */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project facilitates a robust mentorship platform for SVSU    */
/* CSIS students by providing tools for mentor and mentee management */
/* and interactions through a comprehensive web interface.           */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the logic for rendering the user-specific      */
/* dashboard, handling various user roles and displaying appropriate */
/* data based on user status and permissions within the mentorship   */
/* program.                                                          */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - HttpRequest: Class for handling HTTP requests                   */
/* - loader: Module to load Django templates                         */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

import os
from django.http import HttpResponse
from django.template import loader
from mentorship_program_app.models import *
from .admin_dashboard_route import admin_dashboard
from .status_codes import bad_request_400
from utils import security
from .emails import *
from ..models import *
from django.db.models import *
from .filters import *

@security.Decorators.require_login(bad_request_400)
def dashboard(req):
    """
    Function to render the user dashboard based on their role (Mentor or Mentee) and permissions.

    Parameters:
    - req : HttpRequest: The HTTP request object containing user session and permissions.

    Returns:
    - HttpResponse: The rendered HTML for the dashboard page, tailored to the user's role and status.

    This function dynamically builds the dashboard by querying user-related data,
    handling user permissions, and rendering data specific to the user's role within the mentorship program.
    """
    template = loader.get_template('dashboard/dashboard.html')
    session_user = User.from_session(req.session).sanitize_black_properties()
    #8=========D~~~
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
            str_role='Mentor',
            bln_active=True
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

    
    # Retrieve a list of recommended users
    recommended_users = session_user.get_recomended_users()

    if session_user.is_mentor():
        card_data = card_data.exclude(mentee__mentor__id = session_user.mentor.id)
    elif session_user.is_mentee() and session_user.mentee.mentor:
        card_data = card_data.exclude(mentor__id=session_user.mentee.mentor.id)
        
    users = [user.sanitize_black_properties() for user in card_data]
    
    # Moved up for use in interests_with_role_count
    user_ids = [user.id for user in users]
    
    # Get interests as well as counts for filterable users with that interests
    interests_with_role_count = Interest.objects.annotate(
                                    mentor_count=Count('user', filter=Q(user__str_role=opposite_role) & Q(user__id__in=user_ids))
                                    ).values('strInterest', 'mentor_count')   


    users_with_profile = {}
    for user in users:
        page_owner_profile_url = user.profile_img.img.url
        if not os.path.exists(str(settings.MEDIA_ROOT) + page_owner_profile_url.replace("/media", "")):
            page_owner_profile_url = "/media/images/default_profile_picture.png"

        users_with_profile[user.id] = page_owner_profile_url


    # page_owner_profile_url = page_owner_user.profile_img.img.url
    # if not os.path.exists(str(settings.MEDIA_ROOT) + page_owner_profile_url.replace("/media", "")):
    #     page_owner_profile_url = "/media/images/default_profile_picture.png"
    
    #cache the result of this query so we are not using it in the rendered view
    context = {
                                # Making sure that there are enough users to display
            "recommended_users": recommended_users[0:4] if len(recommended_users) >= 4 else recommended_users[0:len(recommended_users)], 
            "all_users"        : users,
            "users_with_profile": users_with_profile,
            "interests"        : list(interests_with_role_count),
            "session_user"     : session_user,
            "role"             : role
    }
    render = template.render(context, req)
    return HttpResponse(render)
