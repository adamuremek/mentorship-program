"""
FILE NAME: deactivate_inactive_accounts.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
FILE PURPOSE:

A script meant to run daily to mark inactive accounts as such after 180 days.

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

"""

from ..models import User
from ..models import SystemLogs
from datetime import date
from dateutil import relativedelta

def run():
    #Get a list of all active users who have not logged in in the last 6 months
    inactive_users = User.objects.filter(str_last_login_date__lte=date.today() - relativedelta(days=180), bln_account_disabled=False, bln_active=True)

    int_count = 0
    for user in inactive_users:
        #Set inactive
        user.bln_active = False
        user.cls_active_changed_date = date.today()
        user.save()
        #Record logs
        SystemLogs.objects.create(str_event=SystemLogs.Event.user_DEACTIVATED, specified_user=user)
        count = count + 1

    print(f"Deactivated {count} accounts.")