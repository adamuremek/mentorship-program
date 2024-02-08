"""
this file contains functions that are only here to make the development environment
easier :D, any code that the end user should NEVER have to see should go here

additionally, functions in this
"""
from mentorship_program_app.models import Users
from .security import Decorators
from .security import is_in_debug_mode



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

    print_debug("[*] generating users...")

    #TODO: these random usas ain't very random boas, 
    #betta get that looked inta
    for i in range(amount):
        new_user = Users.create_from_plain_text_and_email(
                                                f'password{i}',
                                                f'user{i}@sharklazers.com'
                                                )
        new_user.save()

    print_debug('[*] finished random user generation!\n\tenjoy the data :)')



