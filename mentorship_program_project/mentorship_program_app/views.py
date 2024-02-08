from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from utils import development
from utils import security

def default(req):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, req))

def landing(req):
    template = loader.get_template('landing_page.html')
    context = {}
    return HttpResponse(template.render(context, req))

# Pho Post handler for landing-page login card
def landingPost(req):
    if req.method == 'POST':
        return redirect('dashboard')
    else:
        return redirect('landing')

def dashboard(req):
    template = loader.get_template('dashboard/dashboard.html')
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

def profileCard(req):
    template = loader.get_template('dashboard/profile-card/mentor_card.html')
    
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))

# TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING
def role_selection(request):
    template = loader.get_template('sign-in card/role_selection.html')
    context = {}
    return HttpResponse(template.render(context, request))


def account_activation_mentee(request):
    template = loader.get_template('sign-in card/account_activation_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_invalid_mentee(request):
    template = loader.get_template('sign-in card/account_activation_invalid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_valid_mentee(request):
    template = loader.get_template('sign-in card/account_activation_valid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_creation_1_mentee(request):
    template = loader.get_template('sign-in card/account_creation_1_mentee.html')
    context = {
        'pronounlist': ['he', 'she', 'they'],
    }
    return HttpResponse(template.render(context, request))

def account_creation_2_mentee(request):
    template = loader.get_template('sign-in card/account_creation_2_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_mentor(request):
    template = loader.get_template('sign-in card/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))


#please make it pretty front end :)
def invalid_request_401(request):
    response = HttpResponse('Unauthorized') #better 401 page here
    
    response.status_code = 401
    return response

# development only views, these should be removed before production
# still if they are forgotten they should automatically redirect
# when not in DEBUG mode
@security.Decorators.require_debug(invalid_request_401)
def generate_random_user_data(req):
    development.print_debug('running the function')
    #there is no reason to import this in the global file, 
    #as it will only be used when we use the program in dev mode
    #if you feel strongly against this feel free to move it up
    #to the top and include unecessary dependencies in views.py >_>
    
    #
    development.populate_database_with_random_users()

    return HttpResponse('im alive, front en')


