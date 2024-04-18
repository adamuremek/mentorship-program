#django imports
from django.db import models
from django.db.models import *

#project imports
from .svsu_model import SVSUModelData
from django.utils import timezone

from .system_logs import SystemLogs
from .user import User


class UserReport(SVSUModelData,Model):
    """
    Description
    -----------
    UserReport is a database access object.
    This class represents a report for a user.

    Properties
    ----------
    - user (ForeignKey): Represents a user being reported.

    Instance Functions
    ------------------
    - create_user_report: Creates a report in the database using the report type, body,and user's ID.
    - get_report_id: Returns a specified report using an ID.
    - get_reoort_info: Returns a dictionary containing the fields of the report.

    Static Functions
    ----------------
    - get_unresolved_reports_grouped_by_user: Returns a dictionary of all users with unresolved reports.
    - resolve_report: Marks a report as resolved in the database.

    Magic Functions
    ---------------
    - NONE -

    Authors
    -------
    Adam C.
    Jordan A.
    """
    class ReportType(TextChoices):
        """
        Description
        -----------
        An enum subclass to hold the different types of reports

        Properties
        ----------
        - BEHAVIOR

        Instance Functions
        -------------------
        (None)

        Static Functions
        -------
        (None)

        Magic Functions
        -------------
        (None)

        Authors
        -------
        Adam C.
        Jordan A.
        """
        CONDUCT = 'Conduct'
        PROFILE = 'Profile'
        RESPONSIVENESS = 'Responsiveness'
        OTHER = 'Other'

    user = ForeignKey(
        User,
        on_delete = models.CASCADE
    )

    str_report_type = CharField(max_length=15, choices=ReportType.choices, default='')
    str_report_body = CharField(max_length = 3500)
    bln_resolved = BooleanField(default=False)
    date_resolved = DateField(null=True)
    date_reported = DateField(default=timezone.now)
    resolved_comment = CharField(max_length=3500, null=True)

    def create_user_report(reporter: User, str_provided_report_type: str, str_provided_report_body: str, int_user_id: int) -> bool:
        """
        Description
        -----------
        Creates a user report using the report type, body, and user's ID.

        Parameters
        ----------
        - str_provided_report_type (str): The type of report.
        - str_provided_report_body (str): The body of the report.
        - int_user_id (int): ID of user being reported.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - True (boolean): IF the user report was sucessfully created.
        - False (boolean): IF the user report was NOT created.

        Example Usage
        -------------
        >>> boolFlag = create_user_report('Accidentally', '', 24)
        boolFlag = False
        >>> boolFlag = create_user_report('Incident', 'Mentor was rude', 4)
        boolFlag = True

        Authors
        -------
        Adam C.
        """
        try:
            user = User.objects.get(id=int_user_id)
            report = UserReport.objects.create(
                str_report_type = str_provided_report_type,
                str_report_body = str_provided_report_body,
                user = user,
                bln_resolved = False,
            ).save()

            SystemLogs.objects.create(str_event=SystemLogs.Event.REPORT_CREATED_EVENT, specified_user=user, str_details=f"Reported by: {reporter.id}, Report: {report.id}")
            return True
        except Exception as e:
            return False
        
    def get_report_id(int_report_id: int) -> 'UserReport':
        """
        Description
        -----------
        - Gets a UserReport object specified by it's ID.

        Parameters
        ----------
        -int_report_id (int): An integer specifying an object in the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - A UserReport object.
        - Nothing if the requested UserReport object does not exist.

        Example Usage
        -------------
        >>> cls_Report = get_report_id(2)
        cls_Report.str_report_type = 'Incident'
        cls_Report.str_report_body = 'Mentor was rude'
        cls_Report.user_id = 4

        Authors
        -------
        Adam C.
        """
        return UserReport.objects.get(id = int_report_id)
    
    def get_user_report_info(int_report_id: int) -> dict:
        """
        Description
        -----------
        - Gets a specified UserReport by it's ID.
        - Returns a dictionary containing the report type, body, user's ID, and resolved status.

        Parameters
        ----------
        - int_report_id (int): Integer specifying the id of a UserReport in
            the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - dict_Report (Dictionary, String): containing the report type, body, userID and resolved status.

        Example Usage
        -------------
        >>> dict_Report = get_report_id(2)
        dict_Report = {'reportType': 'Incident', 'reportBody': 'Mentor was rude', 'user_id': 4, 'is_resolved': False}

        Authors
        -------
        Adam C.
        """
        cls_Report =  UserReport.get_report_id(int_report_id)

        dict_Report = {
            "report_type" : cls_Report.str_report_type,
            "report_body" : cls_Report.str_report_body,
            "user_id"     : cls_Report.user_id,
            "is_resolved" : cls_Report.bln_resolved
        }

        return dict_Report
    
    @staticmethod
    def get_unresolved_reports_grouped_by_user() -> dict[User, list]:
        """
        Description
        -----------
        - Gets a list of all UserReports
        - Returns a dictionary of user: list[reports].

        Parameters
        ----------
        - NONE -

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
         - dict[User, list[UserReport]]
            A dictionary where the keys are Users and the values are lists of UserReports.

        Example Usage
        -------------
        >>> user_reports_dict = get_reports_grouped_by_user()
        user_reports_dict = {
            <User object>: [<UserReport object (3)>, <UserReport object (4)>],
            <User object>: [<UserReport object (1)>, <UserReport object (2)>],
            ...
        }

        Authors
        -------
        Quinn F.
        """

        # TODO: make this less cursed
        users_with_reports = User.objects.annotate(report_count=Count('userreport', filter=Q(userreport__bln_resolved=False))).filter(report_count__gt=0).prefetch_related('userreport_set')
        user_reports_dict: dict[User, list[UserReport]] = {user: list(user.userreport_set.all().filter(bln_resolved=False)) for user in users_with_reports}
        return user_reports_dict
    
    def get_all_reports_grouped_by_user() -> dict[User, list]:
        users_with_reports = User.objects.annotate(report_count=Count('userreport')).filter(report_count__gt=0).prefetch_related('userreport_set')
        user_reports_dict: dict[User, list[UserReport]] = {user: list(user.userreport_set.all()) for user in users_with_reports}
        return user_reports_dict
    
    @staticmethod
    def get_resolved_reports_grouped_by_user() -> dict[User, list]:
        
        # TODO: make this less cursed
        users_with_reports = User.objects.annotate(report_count=Count('userreport', filter=Q(userreport__bln_resolved=True))).filter(report_count__gt=0).prefetch_related('userreport_set')
        user_reports_dict: dict[User, list[UserReport]] = {user: list(user.userreport_set.all().filter(bln_resolved=True)) for user in users_with_reports}
        return user_reports_dict
    
    # is never called :C
    @staticmethod
    def resolve_report(int_report_id: int, resolver: User):
        """
        Description
        -----------
        - Marks a report as resolved in the database.

        Parameters
        ----------
        - int_report_id (int): The ID of the report to be resolved.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - NONE -

        Example Usage
        -------------
        >>> resolve_report(2)

        Authors
        -------
        Quinn F.
        """

        report = UserReport.get_report_id(int_report_id)
        report.bln_resolved = True
        report.save()