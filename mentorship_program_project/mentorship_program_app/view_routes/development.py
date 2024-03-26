"""
contains views that should only be accessable in development mode
"""
from django.http import HttpRequest, HttpRequest,HttpResponse
from django.template import loader

from utils import security
from utils import development
from utils.development import print_debug

from .status_codes import bad_request_400 as invalid_request_401

from mentorship_program_app.models import User

@security.Decorators.require_debug(invalid_request_401)
def test_database_speed(req : HttpRequest):
    #try uncommenting the select_related for a demonstration of speed up
    users = User.objects.all().prefetch_related("interests").select_related("mentee").select_related("mentor")
    for u in users:
        print(u.str_full_name + " : " + str([i.strInterest for i in u.interests.all()]))
        print(u.is_mentee())
        print(u.is_mentor())
    #return HttpResponse("test concluded")

@security.Decorators.require_debug(invalid_request_401)
def show_all_relationships(req : HttpRequest)->HttpResponse:
    development.show_database_mentorships()
    return HttpResponse("look at the terminal ya goober >:p")

@security.Decorators.require_debug(invalid_request_401)
def display_all_user_roles(request)->HttpResponse:
    """
    Description
    ___________

    simply displayes user roles to the console for debuging :)

    Usage
    _____

    >>> display_all_user_roles(req)

    you can also go to "dev/show_all_user_roles"
    in the app to get a page displaying the roles and print out on console

    Authors
    _______
    David Kennamer 0.0 😹
    """
    ret_val = ""
    for u  in User.objects.all(): 
        role_string = f"{u.cls_email_address} {u.str_first_name} id: {u.id} has a role of : {u.str_role}"
        ret_val +=  role_string  + "\n"
        print(role_string)
    return HttpResponse(role_string)

@security.Decorators.require_debug(invalid_request_401)
def profile_picture_test(request):
    context = {
                "users":[
                    u.sanitize_black_properties() for u in User.objects.all()
                ]
            }
    
    template = loader.get_template('dev/user_images.html')
    
    return HttpResponse(template.render(context,request))

@security.Decorators.require_login(invalid_request_401)
@security.Decorators.require_debug(invalid_request_401)
def is_logged_in_test(request):
    u = User.from_session(request.session)
    return HttpResponse(f"you are currently logged in as {u.str_first_name}, and is a mentee={u.is_mentee()} id={u.id}")



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

