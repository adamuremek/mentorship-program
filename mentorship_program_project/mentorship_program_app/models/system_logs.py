from datetime import timezone
from django.forms import CharField, DateField, DateTimeField
from django.db import models
from django.db.models import *
from .svsu_model import SVSUModelData
from django.utils import timezone

class SystemLogs(SVSUModelData,Model):
    """
    Description
    -----------
    A class to system events

    Properties
    ----------
    - str_event (str): A description of the event that occurred 
    - cls_log_created_on (date): The date the event occured.

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
    
    """
    
    class Event(TextChoices):
        """
        Description
        -----------
        An enum subclass to hold the different user roles

        Properties
        ----------
        - LOGON_EVENT
        - CREATE_MENTORSHIP_EVENT
        - REQUEST_MENTORSHIP_EVENT
        - MENTEE_REGISTER_EVENT
        - MENTOR_REGISTER_EVENT
        - USER_DEACTIVATED

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
        
        """
        LOGON_EVENT = "User logged on"
        APPROVE_MENTORSHIP_EVENT = "Create mentorship"
        REQUEST_MENTORSHIP_EVENT = "Request mentorship"
        MENTORSHIP_TERMINATED_EVENT = "Mentorship terminated"
        MENTEE_REGISTER_EVENT = "Mentee signed up"
        MENTOR_REGISTER_EVENT = "Mentor applied"
        MENTEE_DEACTIVATED_EVENT = "Mentee deactivated"
        MENTOR_DEACTIVATED_EVENT = "Mentor deactivated"
        INTERESTS_CREATED_EVENT = "Interest created"
        INTERESTS_UPDATED_EVENT = "Interest updated"
        INTERESTS_DELETED_EVENT = "Interest deleted"
        MENTOR_APPROVED_EVENT = "Mentor approved"
        MENTOR_DENIED_EVENT = "Mentor denied"
        REPORT_RESOLVED_EVENT ="Report resolved"
        REPORT_CREATED_EVENT = "Report created"
        MENTEE_INACTIVATED_EVENT = "Mentee inactivated"
        MENTOR_INACTIVATED_EVENT = "Mentor inactivated"
        ORGANIZATION_DELETED_EVENT = "Organization deleted"
        ORGANIZATION_CREATED_EVENT = "Organization added"
        MENTOR_ORGANIZATION_CHANGED_EVENT = "Mentor's organization changed"
        AUTO_RESOLVE_EVENT = "User's reports were resolved automatically"
        
    str_event = CharField(max_length=500, choices=Event.choices, default='')
    str_details = CharField(max_length=500, default='')
    cls_log_created_on = DateField(default=timezone.now)
    cls_log_created_on_sortable = DateTimeField(default=timezone.now)
    specified_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)