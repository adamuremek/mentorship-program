# honestly don't know if any of these are used, but im afraid to get rid of them - Andrew
# these can probably go to sign up, but theyre fine here, they are used
from django.http import HttpResponse
from django.template import loader
from mentorship_program_app.models import *
from .emails import *
from ..models import *
def profileCard(req):
    template = loader.get_template('dashboard/profile-card/mentor_card.html')
    
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))

# TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING --ANTHONY PETERS
def role_selection(request):
    template = loader.get_template('sign-in card/shared/role_selection.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_activation_invalid_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_invalid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_valid_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_activation_valid_mentee.html')
    context = {
        'email':'demoemail@something.com'
    }
    return HttpResponse(template.render(context, request))

def account_activation_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))




# -------------------- <<< Big Move stuff >>> -------------------- #
# - Will delete later

# Here lies the 
# so i can delete them?
# the end of an era

# o7
# Here lies the ashes of an era
# THEBIGMOVE will be remembered, not only for its supreme functionality
#   but for the statement it made in its existence.
# THEBIGMOVE will love on in our hearts for generations to unfold <3
#   - Logan Z.
#       Supreme Creator of THEBIGMOVE
