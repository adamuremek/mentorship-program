import json
from django.http import HttpResponse, HttpRequest
from django.template import loader, Template
from django.shortcuts import render, redirect

from utils import development
from utils.development import print_debug
from utils import security
from .status_codes import bad_request_400

from ..models import User
from ..models import Mentor
from ..models import Mentee
from ..models import Interest



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

    user = User.from_session(req.session)

    data = []
    
    if user.is_mentor():
        data = [m.account for m in Mentee.objects.all()]
    else:
        data = [m.account for m in Mentor.objects.all()]

    context = {
            'session_user' : user.sanatize_black_properties(),
            'recommended_users': [u.sanatize_black_properties() for u in data[0:4]],
            'all_users'        : [u.sanatize_black_properties() for u in data]
               }

    return HttpResponse(template.render(context, req))

def admin_dashboard(req):
    context = {}
    return HttpResponse(template.render(context, req))
