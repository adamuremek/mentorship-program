from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect


def BIGMOVE(req):
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def THEBIGMOVE(req):
    template = loader.get_template('sign-in card/single_card_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def THESECONDMOVE(req):
    template = loader.get_template('sign-in card/single_card_mentee.html')
    context = {}
    return HttpResponse(template.render(context, req))

def fuck(req):
    if req.method == 'POST':
        for i in range(2):
            print("-----------")
        print(req.POST)
        for i in range(2):
            print("----------")
        return redirect('landing')


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
