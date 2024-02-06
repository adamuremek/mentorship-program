from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect


# Create your views here.

##LANDING
def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())


##LOGIN PAGE
def login(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())




###NOT WORKING CRSF ERROR
def success(request):
    if request.method == 'POST':
            return render(request, 'index.html')
   
        
 ######
    ## USE BCRYPT
    ### 
       
   





##FROM LOGAN

def default(req):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, req))

def landing(req):
    template = loader.get_template('landing_page.html')
    context = {}
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
    context = {}
    return HttpResponse(template.render(context, request))
