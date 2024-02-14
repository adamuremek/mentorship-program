from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect


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

def admin_dashboard(req):
    template = loader.get_template('admin_dashboard.html')
    context = {}
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

def account_creation_3_mentee(request):
    template = loader.get_template('sign-in card/account_creation_3_mentee.html')
    context = {
        'interestlist': [
            'Artificial Intelligence', 
            'Computer Graphics', 
            'Data Structures & Algorithms',
            'Networking',
            'Operating Systems',
            'Embedded Systems',
            'Cloud Computing',
            'Software Engineering',
            'Distrubuted Systems',
            'Game Development',
            'Cybersecruity',
            'System Analysis'],
    }
    return HttpResponse(template.render(context, request))

def account_creation_4_mentee(request):
    template = loader.get_template('sign-in card/account_creation_4_mentee.html')
    context = {
        'useragreement': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    }
    return HttpResponse(template.render(context, request))


def account_activation_mentor(request):
    template = loader.get_template('sign-in card/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_creation_0_mentor(request):
    template = loader.get_template('sign-in card/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_creation_1_mentor(request):
    template = loader.get_template('sign-in card/account_creation_1_mentor.html')
    context = {
        'pronounlist': ['he', 'she', 'they'],
    }
    return HttpResponse(template.render(context, request))

def account_creation_2_mentor(request):
    template = loader.get_template('sign-in card/account_creation_2_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))