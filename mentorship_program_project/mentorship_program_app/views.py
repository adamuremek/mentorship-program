import json
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from utils import development
from utils.development import print_debug
from utils import security

from .models import User
from .models import Interest
from .models import Mentor
from .models import MentorshipRequest


def request_mentor(request):
    strRequest = "request"
    strMentor = "mentor_id"
    strMentee = "mentee_id"
    boolResponse = False

    if request.method == 'POST':
        """
        I currently have no idea the format frontend will use to pass the data here.
        So, make the changes as needed.
        """

        #Get the data from the POST request.
        data = request.POST
        #Get the action that should be performed.
        action = data.get(strRequest)

        if action == strRequest:
            #User is making a request.
            boolResponse = MentorshipRequest.createRequest(data.get(strMentor), data.get(strMentee))
        else:
            #Else the user is recending the request.
            boolResponse = MentorshipRequest.removeRequest(data.get(strMentor), data.get(strMentee))
    else:
        #PLACEHOLDER
        return HttpRequest("Something happened!")


# -------------------- <<< Big Move stuff >>> -------------------- #
# - Will delete later

#please make it pretty front end :)
def invalid_request_401(request):
    response = HttpResponse('Unauthorized') #better 401 page here
    
    response.status_code = 401
    return response

def BIGMOVE(req):
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

def THEBIGMOVE(req):
    template = loader.get_template('sign-in card/single_page_mentor.html')
    context = {
        'pronounlist': ['he', 'she', 'they']
    }
    return HttpResponse(template.render(context, req))

def THESECONDMOVE(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    context = {}
    return HttpResponse(template.render(context, req))

def register_mentee(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
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
        
        'pronounlist': ['he', 'she', 'they'],
        
        'useragreement': 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",

    }
    return HttpResponse(template.render(context, req))

def register_mentor(req):
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, req))

# --- #
# --- #
# --- #

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

@security.Decorators.require_login(invalid_request_401)
def dashboard(req):
    template = loader.get_template('dashboard/dashboard.html')

    data = User.objects.all()

    context = {
            'recommended_users': [u.sanatize_black_properties() for u in data[0:4]],
            'all_users'        : [u.sanatize_black_properties() for u in data]
               }

    return HttpResponse(template.render(context, req))

#make sure that we are a logged in mentee
#@User.require_loggedin_mentee(invalid_request_401)
#def request_mentor(req):
#    mentor_id = req.get("mentor_id")
#   
#    #ensure that the id exists and that it belongs to a mentor
#    mentor = None
#    try:
#        mentor = User.objects.get(id=mentor_id)
#    except ObjectDoesNotExist:
#        return invalid_request_401(req)
#
#    if not mentor.is_mentor():
#        return invalid_request_401(req)
#
#    security.get_user_id_from_session(req.session)





def admin_dashboard(req):
    context = {}
    return HttpResponse(template.render(context, req))

def profileCard(req):
    template = loader.get_template('dashboard/profile-card/mentor_card.html')
    
    items = range(4)
    context = {'items':items}
    return HttpResponse(template.render(context, req))

#please make pretty front end we love you :D
def home(req):

    return HttpResponse('theres no place me')

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

def account_creation_1_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_creation_1_mentee.html')
    context = {
        'pronounlist': ['he', 'she', 'they'],
    }
    return HttpResponse(template.render(context, request))

def account_creation_2_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_creation_2_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_creation_3_mentee(request):
    template = loader.get_template('sign-in card/mentee/account_creation_3_mentee.html')
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
    template = loader.get_template('sign-in card/mentee/account_creation_4_mentee.html')
    context = {
        'useragreement': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    }
    return HttpResponse(template.render(context, request))


def account_activation_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_creation_0_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_creation_0_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account_creation_1_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_creation_1_mentor.html')
    context = {
        'pronounlist': ['he', 'she', 'they'],
    }
    return HttpResponse(template.render(context, request))

def account_creation_2_mentor(request):
    template = loader.get_template('sign-in card/mentor/account_creation_2_mentor.html')
    context = {}
    return HttpResponse(template.render(context, request))




@security.Decorators.require_login(invalid_request_401)
def logout(request):
    if security.logout(request.session):
        return HttpResponse("logged out!")
    
    #TODO: redirect this to a correct form
    response = HttpResponse("an internal error occured, unable to log you out, STAY FOREVER")
    response.status_code = 500
    return response



#login stuff

def login_uname_text(request):
    login_data = json.loads(request.body.decode("utf-8"))

    uname    = login_data["username"] if "username" in login_data else None
    password = login_data["password"] if "password" in login_data else None
    
    print_debug("uname " + uname)
    print_debug("password " + password)

    if not User.check_valid_login(uname,password):
        response = HttpResponse(json.dumps({"warning":"invalid creds"}))
        response.status_code = 401
        return response
    
    #valid login
    security.set_logged_in(request.session,User.objects.get(clsEmailAddress=uname).id)
    response = HttpResponse(json.dumps({"new_web_location":"/dashboard"}))
    return response





# development only views, these should be removed before production
# still if they are forgotten they should automatically redirect
# when not in DEBUG mode

@security.Decorators.require_debug(invalid_request_401)
def profile_picture_test(request):
    context = {
                "users":[
                    u.sanatize_black_properties() for u in User.objects.all()
                ]
            }
    
    template = loader.get_template('dev/user_images.html')
    
    return HttpResponse(template.render(context,request))

@security.Decorators.require_login(invalid_request_401)
@security.Decorators.require_debug(invalid_request_401)
def is_logged_in_test(request):
    return HttpResponse("you are currently logged in!")



@security.Decorators.require_debug(invalid_request_401)
def test_database_setup(request):
    development.test_database()
    return HttpResponse('finished test sucesfully')



@security.Decorators.require_debug(invalid_request_401)
def generate_random_user_data(request):
    development.print_debug('running the function')
    development.populate_database_with_random_users()
    return HttpResponse('finished generating user data, enjoy controlling the populus :D')

@security.Decorators.require_debug(invalid_request_401)
def populate_default_interest_values(request):
    development.print_debug("[*] generating interests in the database...")
    development.populate_database_with_interests()
    development.print_debug("[*] finished genereating interests! Enjoy the data :)")
    return HttpResponse("finished populating interests in the database!")

@security.Decorators.require_debug(invalid_request_401)
def delete_users(request):
    development.print_debug("[*] are you sure you want to replace all users?")
    if input("(y/n)> ").lower() == 'y':
        User.objects.all().delete()
        return HttpResponse("deleted all user sucessfully >:]")
    return HttpResponse("canceled action!")

@security.Decorators.require_debug(invalid_request_401)
def test_login_page(request):
    template = loader.get_template("dev/test_login.html")
    return HttpResponse(template.render({},request))

