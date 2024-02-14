import bcrypt
from django.conf import settings
from typing import Callable

"""
nulls all objects that are inside of the black list to purge
data for front end, this modifies in place, do not use it if 
you inteand to use the data that gets cleared out. Once used,
you aint' coming back!
"""
def black_list(data : object, black_listed_keys : [str])->None:
    for key in data.__dict__:
        if key in black_listed_keys:
            data.__dict__[key] = None

#returns true if the project is in debug mode
def is_in_debug_mode()->bool:
    return settings.DEBUG

"""
this file is the one stop shop for security functins and things that 
we are afraid we could mess up the math with ;)

make sure any basic securty related functions goes in here so we only have
to change things in one place to fix stuff up
"""


"""
"peppering" a password string is a technique that can provide
a moderate level of additional security in the hashing process by 
removing dependencies on database leaks.

See: https://security.stackexchange.com/questions/17421/how-to-store-salt
for more information regaurding salting and peppering
"""
strPepper : str = """peter pipper 
            picked a 
            pack of 
            pickled peppers 
            to replace 
            this text 
            and make it more secure :D"""
"""
returns a randomly generated salt

the idea is if in the future we need to move from bcrypt we can do so 
since its wrapped
"""
def generate_salt()->str:
    return bcrypt.gensalt()

"""
    hashes an incoming plain text password using the applications built in pepper and 
    provided salt.
    In order for the peppering to work this should be the one stop shop for hashing
"""
def hash_password(password_plain_text : str,salt : str)->str:
    pepperd_password = password_plain_text + strPepper
    return bcrypt.hashpw(pepperd_password.encode('UTF-8'),salt)

"""
pythonic "namespace" for the decorators contained in the security file
"""
class Decorators:
    """
    generates a decorator that will test the given function by the given choice,
    and swap out the function for alternative if it fails that choice

    the code for this kind of thing looks nasty, but it is SO nice to use 
    after you get pasted the cursed defs in defs

    --------------------------------------------------------------
    USAGE EXAMPLE:

    def invalid_login_view(req):
        ...
        ...

    @require_check(lambda req : req.session[0] == 'login',invalid_login_view)
    def some_view(req):
        ...
        ...
        ...

    --------------------------------------------------------------

    NOTE: 

    while the example shows how to use this method for login systems,

    there is another decorator in this file SPECIFICALLY for that purpose in the form
    of require_logged_in. 

    It is STRONGLY encouraged to use the require_logged_in function 
    so that the login code is properly parsed

    """
    def require_check(check : Callable[[],bool],alternate : callable)->callable:
        
        #takes in a given function, and augments it
        #to return its standard value if the check is true,
        #and an alternate value if the check is false
        def check_decorator(decorated_function : Callable )->callable:
            
            def return_function(*args):
                if len(args) < 0:
                    return alternate(*args)

                first_arg = args[0]

                if check(first_arg):
                    return decorated_function(*args)
                return alternate(*args)
                #end the inner function that contains the actual behavor

            return return_function
            #end the decorator that returns the inner function

        return check_decorator
        #end the function that creates the decorator

    """
    decorator that makes it so that a given function will only be called if the user 
    is logged in properly 


    ---------------------------------------------------
    USAGE:

    def invalid_login_view(req):
        ...
        ...
        ...

    @require_login(invalid_login_view)
    def some_view(reqs):
        ...
        ...

    """
    def require_login(alternate_view):
        return Decorators.require_check(lambda req : req.session.get('login',False),
                             alternate_view)

    """
    decorator that requires the program be in debug mode in order to work properly

    ---------------------------------------------------
    USAGE:

    def invalid_login_view(req):
        ...
        ...
        ...

    @require_debug(invalid_login_view)
    def some_view(reqs):
        ...
        ...

    """
    def require_debug(alternate_view):
        return Decorators.require_check(lambda _ : is_in_debug_mode(),alternate_view)


