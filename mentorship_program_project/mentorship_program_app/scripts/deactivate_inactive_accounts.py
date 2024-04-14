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

>>> python deactive_inactive_accounts.py
"Deactivated 7 accounts."

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT
WJL 4/2/2024   Created the script
"""

from ..models import User
from ..models import SystemLogs
from datetime import date
from dateutil.relativedelta import relativedelta
from ..view_routes.emails import *

def run() -> None:
    """
    Description
    -----------
    Sets any user that has not signed in 6 months to be inactive

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - None

    Example Usage
    -------------

    >>> python deactivate_inactive_accounts.py
    "Deactivated 5 accounts."

    Authors
    -------
    William L:pscomb
    """
    #Get a list of all active users who have not logged in in the last 6 months
    inactive_users = User.objects.filter(str_last_login_date__lte=date.today() - relativedelta(days=180), bln_account_disabled=False, bln_active=True)
    soon_to_be_inactive_users = User.objects.filter(str_last_login_date=date.today() - relativedelta(days=173), bln_account_disabled=False, bln_active=True)

    for user in soon_to_be_inactive_users:
        account_deactivating_soon(user.cls_email_address)

    count = 0
    for user in inactive_users:
        #Set inactive
        User.make_user_inactive(user, "User was deactivated for being inactive for 180 days")
        user.cls_active_changed_date = date.today()
        user.save()
        count = count + 1
        account_deactivated_email(user.cls_email_address)

    print(f"Deactivated {count} accounts.")