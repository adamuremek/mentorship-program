from django.http import HttpResponse, HttpRequest, FileResponse
from django.template import loader, Template
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from utils import development
from datetime import date, datetime, timedelta
from utils.development import print_debug
from utils import security
from .status_codes import bad_request_400
from django.db.models import Count, Q

from ..models import User
from ..models import Mentor
from ..models import Mentee
from ..models import Interest
from ..models import SystemLogs
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os

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
    

    overall_stats = get_project_overall_statistics()
    timespan_stats = get_project_time_statistics()

    context = {"pending_mentor_count"        : overall_stats["pending_mentor_count"       ],
               "active_mentees_count"        : overall_stats["active_mentees_count"       ],
               "inactive_mentees_count"      : overall_stats["inactive_mentees_count"     ],
               "active_mentors_count"        : overall_stats["active_mentors_count"       ],
               "inactive_mentors_count"      : overall_stats["inactive_mentors_count"     ],
               "mentees_per_mentor"          : overall_stats["mentees_per_mentor"         ],
               "mentor_turnover_rate"        : overall_stats["mentor_turnover_rate"       ],
               "mentor_retention_rate"       : overall_stats["mentor_retention_rate"      ],
               "successful_match_rate"       : overall_stats["successful_match_rate"      ],
               "total_approved_mentorships"  : overall_stats["total_approved_mentorships" ],
               "total_requested_mentorships" : overall_stats["total_requested_mentorships"],
               "unassigned_mentees"          : overall_stats["unassigned_mentees"         ],
               "unassigned_mentors"          : overall_stats["unassigned_mentors"         ],
               
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

def get_project_time_statistics():
    week_ago_date = date.today() - timedelta(days=7)
    month_ago = date.today() - timedelta(days=30)

    daily_stats = (
        SystemLogs.objects.filter(str_event=SystemLogs.Event.LOGON_EVENT, cls_log_created_on=date.today()).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on=date.today()).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on=date.today()).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT, cls_log_created_on=date.today()).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_DEACTIVATED, cls_log_created_on=date.today()).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTOR_DEACTIVATED, cls_log_created_on=date.today()).count(),
    )

    weekly_stats = (
        SystemLogs.objects.filter(str_event=SystemLogs.Event.LOGON_EVENT, cls_log_created_on__gte=week_ago_date).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on__gte=week_ago_date).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on__gte=week_ago_date).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT, cls_log_created_on__gte=week_ago_date).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_DEACTIVATED, cls_log_created_on__gte=week_ago_date).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTOR_DEACTIVATED, cls_log_created_on__gte=week_ago_date).count(),
    )

    monthly_stats = (
        SystemLogs.objects.filter(str_event=SystemLogs.Event.LOGON_EVENT, cls_log_created_on__gte=month_ago).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on__gte=month_ago).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, cls_log_created_on__gte=month_ago).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT, cls_log_created_on__gte=month_ago).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_DEACTIVATED, cls_log_created_on__gte=month_ago).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTOR_DEACTIVATED, cls_log_created_on__gte=month_ago).count(),
    )

    lifetime_stats = (
        SystemLogs.objects.filter(str_event=SystemLogs.Event.LOGON_EVENT).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTEE_DEACTIVATED,).count(),
        SystemLogs.objects.filter(str_event=SystemLogs.Event.MENTOR_DEACTIVATED,).count(),
    )

    return {"Daily":daily_stats, "Weekly":weekly_stats, "Monthly":monthly_stats, "Lifetime":lifetime_stats}


# TODO sorry this look like this. If anyone got free time can you make this "feel" better thanks! -JA
def get_project_overall_statistics():

    inactive_date = datetime.now() - timedelta(days=365)
    # Query to count the number of Mentors who are currently inactive
    inactive_mentors_count = User.objects.filter(str_role='Mentor', str_last_login_date__lt=inactive_date).count()
    # Query to count the number of Mentors who are currently active
    active_mentors_count = User.objects.filter(str_role='Mentor',str_last_login_date__gte=inactive_date).count()
    # Number of total mentees
    total_mentees = User.objects.filter(str_role='Mentee').count()
    # Number of total mentors
    total_mentors = User.objects.filter(str_role='Mentor').count()
    # Total amount of approved mentorships
    total_approved_mentorships = SystemLogs.objects.filter(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT).count()
    # Total amount of requested mentorships
    total_requested_mentorships = SystemLogs.objects.filter(str_event=SystemLogs.Event.REQUEST_MENTORSHIP_EVENT).count()
    
    Mentor.objects.filter().count()

    #  user.mentor.account if page_owner_mentee.mentor != None else None
    all_mentees = User.objects.filter(str_role='Mentee')

    # count number of unassigned mentees
    unassigned_mentees = 0
    for mentee in all_mentees:
        if mentee.mentee.mentor_id == None:
            unassigned_mentees += 1

    # count number of unassigned mentors
            #TODO if time, pending mentors also count towards unassigned
    unassigned_mentors = 0
    all_mentors = Mentor.objects.all()
    for mentor in all_mentors:
        if len(mentor.mentee_set.all()) == 0:
            unassigned_mentors += 1

    active_mentors_count = User.objects.filter(str_role='Mentor',str_last_login_date__gte=inactive_date).count()


    return {
        "pending_mentor_count"        : User.objects.filter(str_role='MentorPending').count(),
        "active_mentees_count"        : User.objects.filter(str_role='Mentee', str_last_login_date__gte=inactive_date).count(),
        "inactive_mentees_count"      : User.objects.filter(str_role='Mentee', str_last_login_date__lt=inactive_date).count(),
        "active_mentors_count"        : active_mentors_count,
        "inactive_mentors_count"      : inactive_mentors_count,
        "mentees_per_mentor"          : f"{round(total_mentees/total_mentors,2)}" if total_mentors != 0 else 'N/A',
        "mentor_turnover_rate"        : f"{round((inactive_mentors_count / total_mentors ) * 100)}%" if total_mentors != 0 else 'N/A',
        "mentor_retention_rate"       : f"{round(100 - ((inactive_mentors_count / total_mentors) * 100))}%" if total_mentors != 0 else 'N/A',
        "successful_match_rate"       : f"{round(total_approved_mentorships/total_requested_mentorships * 100)}%" if total_requested_mentorships != 0 else "N/A",
        "total_approved_mentorships"  : total_approved_mentorships,
        "total_requested_mentorships" : total_requested_mentorships,
        "unassigned_mentees"          : unassigned_mentees,
        "unassigned_mentors"          : unassigned_mentors,
    }


def generate_report(req : HttpRequest):
    workbook = Workbook()
    worksheet = workbook.active
    timespans = get_project_time_statistics()

    header = ["Daily Stats", "Weekly Stats", "Monthly Stats", "Lifetime stats"]
    worksheet.merge_cells('A1:B1')
    worksheet.merge_cells('D1:E1')
    worksheet.merge_cells('G1:H1')
    worksheet.merge_cells('J1:K1')
    
    worksheet["A1"] = header[0]
    worksheet["D1"] = header[1]
    worksheet["G1"] = header[2]
    worksheet["J1"] = header[3]

    worksheet["A1"].alignment = Alignment(horizontal="center")
    worksheet["D1"].alignment = Alignment(horizontal="center")
    worksheet["G1"].alignment = Alignment(horizontal="center")
    worksheet["J1"].alignment = Alignment(horizontal="center")

    worksheet.column_dimensions['A'].width = 40
    worksheet.column_dimensions['D'].width = 40
    worksheet.column_dimensions['G'].width = 40
    worksheet.column_dimensions['J'].width = 40

    for column_1, column_2, timespan in (("A", "B", "Daily"), ("D", "E", "Weekly"), ("G", "H", "Monthly"), ("J", "K", "Lifetime")):
        
        worksheet[f"{column_1}2"] = f"{timespan} Visitors"
        worksheet[f"{column_1}3"] = f"{timespan} Mentee Signup"
        worksheet[f"{column_1}4"] = f"{timespan} Mentor Signup"
        worksheet[f"{column_1}5"] = f"{timespan} Assigned Mentees"
        worksheet[f"{column_1}6"] = f"{timespan} Deactivated Mentees"
        worksheet[f"{column_1}7"] = f"{timespan} Deactivated Mentors"
        
        worksheet[f"{column_2}2"] = timespans[timespan][0]
        worksheet[f"{column_2}3"] = timespans[timespan][1]
        worksheet[f"{column_2}4"] = timespans[timespan][2]
        worksheet[f"{column_2}5"] = timespans[timespan][3]
        worksheet[f"{column_2}6"] = timespans[timespan][4]
        worksheet[f"{column_2}7"] = timespans[timespan][5]


    workbook.save('test.xlsx')
    file_path = os.path.join(settings.MEDIA_ROOT, "test.xlsx")
    return  FileResponse(open('test.xlsx', 'rb'), as_attachment=True, filename=file_path)




