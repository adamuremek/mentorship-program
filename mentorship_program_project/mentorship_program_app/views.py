from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from utils import development
from utils import security

from .models import User
from .models import Interest

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
def test_database_setup(request):
    
    development.print_debug("[database test] generating new interests...")
    
    fake_interests = [
            'mario party',
            'minecraft',
            'ghost game',
            'hollow knight',
            'rain world'
            ]
    #make a set of default interests
    for interest in fake_interests:
        development.print_debug(f"[database test] =>\t creating interest {interest}")
        try:
            interest_obj = Interest.objects.create(strInterest=interest)
            interest_obj.save()
        except:
            development.print_debug("[database test] =>\t key already exists")

    development.print_debug(f"[database test] finished generating interests!")
    development.print_debug(f"[database test] reading interests back from the db...")

    mario_party_interest = Interest.objects.get(strInterest='mario party')
    ghost_game_interest  = Interest.objects.get(strInterest='ghost game')
    rainworld_interest   = Interest.objects.get(strInterest='rain world')

    development.print_debug("[database test] sucessfully read interest from the db!")


    development.print_debug("[database test] creating fake users...")
    
    fakeuser1 = None
    try: 
        fakeuser1 = User.create_from_plain_text_and_email('fakeuser1',
                                                          'fakeuser1@fake.com')
    except:
        development.print_debug("fakeuser1 already exists")
        fakeuser1 = User.objects.get(clsEmailAddress='fakeuser1@fake.com')
    
    fakeuser2 = None
    try: 
        fakeuser2 = User.create_from_plain_text_and_email('fakeuser2',
                                                          'fakeuser2@fake.com')
    except:
        fakeuser2 = User.objects.get(clsEmailAddress='fakeuser2@fake.com')
        development.print_debug("fakeuser2 already exists")
    
    fakeuser3 = None
    try: 
        fakeuser3 = User.create_from_plain_text_and_email('fakeuser3',
                                                          'fakeuser3@fake.com')
    except:
        fakeuser3 = User.objects.get(clsEmailAddress='fakeuser3@fake.com')
        development.print_debug("fakeuser3 already exists")

    
    development.print_debug("[database test]=>\t adding interests to the users...")
    #add interests to the users
    fakeuser1.interests.add(mario_party_interest)
    fakeuser1.interests.add(rainworld_interest)
    fakeuser1.interests.add(ghost_game_interest)

    fakeuser2.interests.add(rainworld_interest)
    fakeuser3.interests.add(ghost_game_interest)

    development.print_debug("[database test]=>\t saving new users")
    fakeuser1.save()
    fakeuser2.save()
    fakeuser3.save()


    development.print_debug("[database test] finished user generation!")

    #now lets try and read the data back

    development.print_debug("[database test] printing newly created users")
    
    all_users = User.objects.all()
    development.print_debug(all_users)

    development.print_debug("[database test] displaying user interests!")
    development.print_debug("="*5)
    
    for user in all_users:
        development.print_debug(user.clsEmailAddress)
        user_interests = user.interests.all()
        development.print_debug(user_interests)
        
        for user_int in user_interests:
            development.print_debug("\t "+user_int.strInterest)
        
        development.print_debug("-")


    development.print_debug("[database test] deleting the data....")
    
    fakeuser1.delete()
    fakeuser2.delete()
    fakeuser3.delete()

    #purge all of the fake interests
    Interest.objects.filter(strInterest__in=fake_interests).delete()


    development.print_debug("[database test] finished running, enjoy the data :)")


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
