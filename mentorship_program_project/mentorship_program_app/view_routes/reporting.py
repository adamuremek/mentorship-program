from django.http import HttpRequest, FileResponse
from django.conf import settings
from datetime import date, datetime, timedelta

from ..models import User
from ..models import Mentor
from ..models import SystemLogs
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os

def get_project_time_statistics():
    """
        Authors Andrew P. Jordan A.
        Collect and synthesize data from Systemlogs and output results based on timespans
    """
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
    """
        Authors Andrew P. Jordan A.
        Collect and synthesize data from Systemlogs based on general stats
    """

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
        "active_mentees"              : User.objects.filter(str_role='Mentee', str_last_login_date__gte=inactive_date).count(),
        "unassigned_mentees"          : unassigned_mentees,
        "inactive_mentees"            : User.objects.filter(str_role='Mentee', str_last_login_date__lt=inactive_date).count(),
        "active_mentors"              : active_mentors_count,
        "unassigned_mentors"          : unassigned_mentors,
        "inactive_mentors"            : inactive_mentors_count,
        "mentees_per_mentor"          : f"{round(total_mentees/total_mentors,2)}" if total_mentors != 0 else 'N/A',
        "mentor_retention_rate"       : f"{round(100 - ((inactive_mentors_count / total_mentors) * 100))}%" if total_mentors != 0 else 'N/A',
        "mentor_turnover_rate"        : f"{round((inactive_mentors_count / total_mentors ) * 100)}%" if total_mentors != 0 else 'N/A',
        "total_approved_mentorships"  : total_approved_mentorships,
        "total_requested_mentorships" : total_requested_mentorships,
        "successful_match_rate"       : f"{round(total_approved_mentorships/total_requested_mentorships * 100)}%" if total_requested_mentorships != 0 else "N/A",
        "pending_mentor"              : User.objects.filter(str_role='MentorPending').count(),
    }

def generate_report(req : HttpRequest):
    """
    Authors Andrew P. Jordan A.
    Generate report (duh!)
    """
    workbook = Workbook()
    worksheet = workbook.active
    timespans = get_project_time_statistics()
    overall_stats = get_project_overall_statistics()

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

    worksheet.merge_cells('A9:B9')
    worksheet["A9"] = "Program Statistics"
    worksheet["A9"].alignment = Alignment(horizontal="center")
    for index, stat in enumerate(overall_stats, start=10):
        worksheet[f"B{index}"].alignment = Alignment(horizontal="right")

        worksheet[f"A{index}"] = stat.replace("_", " ").title()
        worksheet[f"B{index}"] = overall_stats[stat]
       

  

    workbook.save(f'Program Statistics{date.today()}.xlsx')
    file_path = os.path.join(settings.MEDIA_ROOT, "test.xlsx")
    return FileResponse(open('test.xlsx', 'rb'), as_attachment=True, filename=file_path)



