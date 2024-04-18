
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.shortcuts import  redirect
from django.core.exceptions import ObjectDoesNotExist
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils import security
from .emails import *
from django.utils import timezone
from ..models import *

from typing import Dict
def resolve_report(req: HttpRequest):
    resolver = User.from_session(req.session)
    if not resolver.is_super_admin():
        return bad_request_400("permission denied!")

    if req.method == "POST":
        # get the id of the report
        id = req.POST["report-id"]
        # get the id of the user who was reported
        user_id = req.POST["user-id"]
        # the comment from the admin
        comment = req.POST["comment"] if req.POST["comment"] != None else "No Comment"
        # decision == true means user was banned
        decision = 'decision' in req.POST
        # get the report


        report = UserReport.objects.get(id=id)
        report.bln_resolved = True
        report.date_resolved = timezone.now()
        report.resolved_comment = comment

        user = User.objects.get(id=user_id)
        SystemLogs.objects.create(str_event=SystemLogs.Event.REPORT_RESOLVED_EVENT, specified_user=user, str_details=f"Handled by: {resolver.id}, Report: {id}")

        # if the user was banned, disable their account, and resolve any other issues they have
        if decision:
            User.disable_user(user, f"User was deactivated from report: {id}")
            # get the other outstanding reports
            other_reports = UserReport.objects.filter(user_id=user_id, bln_resolved=False)
            
            for other_report in other_reports:
                # make sure the report isn't the report we just resolved
                if report.id != other_report.id:
                    other_report.bln_resolved = True
                    other_report.date_resolved = timezone.now()
                    report.resolved_comment = f"Report was resolved because user was banned for: {comment}"
                    other_report.save()
                    SystemLogs.objects.create(str_event=SystemLogs.Event.AUTO_RESOLVE_EVENT, specified_user=user, str_details=f"Report: {other_report.id}")
        report.save()

        

    return redirect("/admin_reported_users/")


@security.Decorators.require_login(bad_request_400)
def report_user(req: HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Creates a new user report

    Parameters
    ----------
    - req (HttpRequest): The request object

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The http response for the redirect

    Example Usage
    -------------
    >>> path('report_user/', backend_requests.report_user, name='report user')

    Authors
    -------
    Quinn F. 
    """

    user = User.from_session(req.session)
    str_error_message = "The following error(s) occured:"
    errors =  []
    errors.append(str_error_message)
    bool_error = False

    try:
        User.objects.get(id=req.POST.get("reported_user_id", None))
    except ObjectDoesNotExist:
        errors.append("Invalid reported user ID.")
        bool_error = True

    if not req.POST.get("report_type", None):
        errors.append("Report type is required.")
        bool_error = True
    
    if not req.POST.get("report_reason", None):
        errors.append("Report reason is required.")
        bool_error = True    
    
    if bool_error:
        return bad_request_400("\n".join(errors))
    else:
        reported_user_id = req.POST['reported_user_id']
        report_type = req.POST['report_type']
        report_reason = req.POST['report_reason']
        UserReport.create_user_report(user, report_type, report_reason, reported_user_id)
        alert_admins_of_reported_user()
        return redirect('/universal_profile/' + reported_user_id)
    

def admin_reported_users(request):
    template = loader.get_template('admin/admin_reported_users.html')

    user_reports_dict = UserReport.get_unresolved_reports_grouped_by_user()
    all_reports = UserReport.get_all_reports_grouped_by_user()
    result = {key: all_reports[key] for key in all_reports if key not in user_reports_dict}
    resolved_reports = UserReport.get_resolved_reports_grouped_by_user()
    

    
    context = {"user_reports_dict": user_reports_dict,
               "all_reports": all_reports,
               "resolved_reports":resolved_reports,
               }
    return HttpResponse(template.render(context,request))
