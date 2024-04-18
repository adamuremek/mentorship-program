from utils import security
from .reporting import *

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
        context['org_admin'] = session_user.is_an_org_admin()

    return context






