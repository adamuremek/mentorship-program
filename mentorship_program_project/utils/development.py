"""
this file contains functions that are only here to make the development environment
easier :D, any code that the end user should NEVER have to see should go here

additionally, functions in this
"""
import random
import string

from utils.security import is_in_debug_mode

from mentorship_program_app.models import Users
from mentorship_program_app.models import Interests



"""
simple function to save time later and not have to hunt down debugs
"""
def print_debug(*args):
    if is_in_debug_mode():
        print(*args)


"""
fills the database with randomly generated users ONLY if in 
debug mode
"""
def populate_database_with_random_users(amount  : int = 100)->None:
    print_debug("[random user generator] ensuring existence of interests...")
    populate_database_with_interests()

    print_debug("[random user generator] generating users...")

    for i in range(amount):
        user = f'user{i}@'+''.join(random.choice(string.ascii_letters)for _ in range(100))+'.com'
        new_user = Users.create_from_plain_text_and_email(
                                                f'password{i}',
                                                user
                                                )
        new_user.save()
        print_debug('[random user generator] finished random user generation!\n\tenjoy the data :) '+user)

"""
populate the database with debug generated interests

if already populated, skip doing that population

this might be better moved into some sort of database file,
but I figure sense this is only used in development mode this 
is an ok place for it for now
"""
def populate_database_with_interests()->None:
    for interest in Interests.getDefaultInterestList():
        if len(Interests.objects.filter(strInterest = interest)) > 0:
            interest_object = Interests.objects.create(strInterest = interest)
            interest_object.save()
            
            print_debug(f'[interest populator] finished with {interest}')
        else:
            
            print_debug(f"[interest populator] {interest} is already in the database")



