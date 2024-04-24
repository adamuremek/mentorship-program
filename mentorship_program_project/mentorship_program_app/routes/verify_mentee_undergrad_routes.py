
from datetime import date

from django.http import HttpResponse, HttpRequest
from django.shortcuts import  redirect
from mentorship_program_app.models import *
from .status_codes import  invalid_request_401
from .emails import *
from ..models import *
from dateutil import relativedelta



@User.Decorators.require_logged_in_super_admin(invalid_request_401)
def verify_mentee_ug_status(req : HttpRequest) -> HttpResponse:
    """
    Description
    -----------
    Sets any mentee that is not an undergrad student to inactive

    NOTE: This implementation is flawed, but the best solution requires getting
    information from IT, which isn't feasible.

    Parameters
    ----------
    - req (HttpRequest): Unused, but required for the decorator

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - HttpResponse: The http reponse for the redirect

    Example Usage
    -------------

    >>> path('verify_mentees/', backend_requests.verify_mentee_ug_status,
            name='verify mentees')
    7

    Authors
    -------
    Andy Do
    William Lipscom:b
    Jordan Anodjo
    """

    inactive_mentees = User.objects.filter(cls_date_joined__lte=date.today() - relativedelta.relativedelta(years=5), str_role="Mentee", bln_account_disabled=False, bln_active=True)

    for mentee in inactive_mentees:
        User.disable_user(mentee, "Mentee was deactivated for not being an undergrad")
        # record logs

    return redirect('/admin_dashboard')