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
from mentorship_program_app.models import Mentee
from mentorship_program_app.models import Mentor



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
def populate_database_with_random_users(amount  : int = 10)->None:
    print_debug("[random user generator] ensuring existence of interests...")
    populate_database_with_interests()

    print_debug("[random user generator] generating users...")


    mentor_threshold_amount = amount / 2

    for i in range(amount):
        user = f'user{i}@fakeemail{i}.com'
        
        new_user = None

        #try:
        new_user = None
        first_name_prefix = ""
        
        if i < mentor_threshold_amount:
            new_user = Mentee.create_from_plain_text_and_email(
                                                f'password{i}',
                                                user
                                                )
            first_name_prefix = "mentee "
        else:
            new_user = Mentor.create_from_plain_text_and_email(
                                                f'password{i}',
                                                user
                                                )
            first_name_prefix = "mentor "
            
        #we specifically want the account from the mentor/mentee class for the following code
        new_user = new_user.account

        new_user.strFirstName = first_name_prefix + random.choice(["Doc","Happy","Grumpy","Sleepy","Dopey","Bashful","Sneezy"])
        new_user.strLastName = random.choice(["Doc","Happy","Grumpy","Sleepy","Dopey","Bashful","Sneezy"])

        #except:
        #    print_debug("that user already exists ya silly goose")
        #    continue #if the user already exists, move onto the next user



        if new_user == None:
            print_debug("[random user generator] WARNING, unkown error occured while generating the user")
            continue
        user_interests = get_random_interests(5)
        new_user.interests.add(*user_interests)

        new_user.save()
        print_debug('[random user generator] ' + user + ' as ' + ('mentor' if new_user.is_mentor() else 'mentee'))

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


"""
generate and test several different users, doesn't actually return true or false for testing 
instead if this fails, ya got problems
"""
def test_database()->None:
    print_debug("[database test] generating new interests...")
    
    fake_interests = [
            'mario party',
            'minecraft',
            'ghost game',
            'hollow knight',
            'rain world'
            ]
    #make a set of default interests
    for interest in fake_interests:
        print_debug(f"[database test] =>\t creating interest {interest}")
        try:
            interest_obj = Interest.objects.create(strInterest=interest)
            interest_obj.save()
        except:
            print_debug("[database test] =>\t key already exists")

    print_debug(f"[database test] finished generating interests!")
    print_debug(f"[database test] reading interests back from the db...")

    mario_party_interest = Interest.objects.get(strInterest='mario party')
    ghost_game_interest  = Interest.objects.get(strInterest='ghost game')
    rainworld_interest   = Interest.objects.get(strInterest='rain world')

    print_debug("[database test] sucessfully read interest from the db!")


    print_debug("[database test] creating fake users...")
    
    fakeuser1 = None
    try: 
        fakeuser1 = User.create_from_plain_text_and_email('fakeuser1',
                                                          'fakeuser1@fake.com')
    except:
        print_debug("fakeuser1 already exists")
        fakeuser1 = User.objects.get(clsEmailAddress='fakeuser1@fake.com')
    
    fakeuser2 = None
    try: 
        fakeuser2 = User.create_from_plain_text_and_email('fakeuser2',
                                                          'fakeuser2@fake.com')
    except:
        fakeuser2 = User.objects.get(clsEmailAddress='fakeuser2@fake.com')
        print_debug("fakeuser2 already exists")
    
    fakeuser3 = None
    try: 
        fakeuser3 = User.create_from_plain_text_and_email('fakeuser3',
                                                          'fakeuser3@fake.com')
    except:
        fakeuser3 = User.objects.get(clsEmailAddress='fakeuser3@fake.com')
        print_debug("fakeuser3 already exists")

    
    print_debug("[database test]=>\t adding interests to the users...")
    #add interests to the users
    fakeuser1.interests.add(mario_party_interest)
    fakeuser1.interests.add(rainworld_interest)
    fakeuser1.interests.add(ghost_game_interest)

    fakeuser2.interests.add(rainworld_interest)
    fakeuser3.interests.add(ghost_game_interest)

    print_debug("[database test]=>\t saving new users")
    fakeuser1.save()
    fakeuser2.save()
    fakeuser3.save()


    print_debug("[database test] finished user generation!")

    #now lets try and read the data back

    print_debug("[database test] printing newly created users")
    
    all_users = User.objects.all()
    print_debug(all_users)

    print_debug("[database test] displaying user interests!")
    print_debug("="*5)
    
    for user in all_users:
        print_debug(user.clsEmailAddress)
        user_interests = user.interests.all()
        print_debug(user_interests)
        
        for user_int in user_interests:
            print_debug("\t "+user_int.strInterest)
        
        print_debug("-")


    print_debug("[database test] deleting the data....")
    
    fakeuser1.delete()
    fakeuser2.delete()
    fakeuser3.delete()

    #purge all of the fake interests
    Interest.objects.filter(strInterest__in=fake_interests).delete()


    print_debug("[database test] finished running, enjoy the data :)")


