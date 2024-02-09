"""
this file contains functions that are only here to make the development environment
easier :D, any code that the end user should NEVER have to see should go here

additionally, functions in this
"""
import random
import string

from utils.security import is_in_debug_mode

from mentorship_program_app.models import User
from mentorship_program_app.models import Interest



"""
simple function to save time later and not have to hunt down debugs
"""
def print_debug(*args):
    if is_in_debug_mode():
        print(*args)


"""
returns an array of randomly selected interests of a given size
"""
def get_random_interests(size : int)->[Interest]:
    random_interest_list = []
    interest_objects = Interest.objects.all()

    #if we have to randomly pick the entire set,
    #then we return, well the set
    if size >= len(interest_objects):
        return interest_objects


    for i in range(size):
        random_choice = random.choice(interest_objects)
        
        while random_choice in random_interest_list:
            random_choice = random.choice(interest_objects)
        
        random_interest_list.append(random_choice)
    
    return random_interest_list

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


        new_user = User.create_from_plain_text_and_email(
                                                f'password{i}',
                                                user
                                                )
        new_user.save()

        user_interests = get_random_interests(5)
        new_user.interests.add(*user_interests)

        print_debug('[random user generator] finished random user generation!\n\tenjoy the data :) '+user)

"""
populate the database with debug generated interests

if already populated, skip doing that population

this might be better moved into some sort of database file,
but I figure sense this is only used in development mode this 
is an ok place for it for now

we might also want to generate this from sql files, this is very much
a "get to the data" quickly solution, altough I suppose having it here 
means we can point admins to this function in a url to re populate the default 
interests
"""
def populate_database_with_interests()->None:
    default_interests = Interest.get_initial_default_interest_strings()
    for interest in default_interests:
        
        try:
            Interest.objects.get(strInterest = interest)
            print_debug(f"[interest populator] {interest} is already in the database")
        except:
            interest_object = Interest.objects.create(strInterest = interest)
            interest_object.save()
            
            print_debug(f'[interest populator] finished with {interest}')



