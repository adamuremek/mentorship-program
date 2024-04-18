import bcrypt
import re
from django.conf import settings
from typing import Callable
from django.http import HttpRequest

from mentorship_program_app.routes.status_codes import bad_request_400
from base64 import b64encode,b64decode

"""
this file is the one stop shop for security functins and things that 
we are afraid we could mess up the math with ;)

make sure any basic securty related functions goes in here so we only have
to change things in one place to fix stuff up
"""

"""
logs the current session out 

returns true if we managed to log out 
the user, false if the user is already logged out 
and the operation had no effect
"""
def logout(session : dict)->bool:
    if is_logged_in(session):
        session["login"] = False
        return True
    return False
"""properly sets the session variable to login"""
def set_logged_in(session : dict,user)->bool:
    
    #TODO: circular imports mean that we can't use the 
    #enumerators here which is EVIL
    #probably we want this security file moved into the 
    #project to avoid that
    if not user.str_role in ['Mentor','Mentee','Admin']:
        return False

    session["login"] = True
    session["user_id"] = user.id
    return True

"""returns true if we are currently logged in, else false"""
def is_logged_in(session : dict)->bool:
    return session["login"] if "login" in session else False

"""
convinence function to return the id of the current user from a given session id
"""
def get_user_id_from_session(session : dict)->int:
    return session["user_id"]

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
    s = b64encode(bcrypt.gensalt())
    return s.decode("UTF-8")


"""
    hashes an incoming plain text password using the applications built in pepper and 
    provided salt.
    In order for the peppering to work this should be the one stop shop for hashing
"""
def hash_password(password_plain_text : str,salt : str)->str:
    salt_data = b64decode(salt)
    pepperd_password = password_plain_text + strPepper

    #anything touching the random number generators needs to be b64 encoded
    #to properly be stored in the database
    ret_val = b64encode(
            bcrypt.hashpw(pepperd_password.encode('UTF-8'),salt_data)
            ).decode('UTF-8')
    return ret_val

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
            
            def return_function(*args,**kwargs):
                if len(args) < 0:
                    return alternate(*args,**kwargs)

                first_arg = args[0]

                if check(first_arg):
                    return decorated_function(*args,**kwargs)
                return alternate(*args,**kwargs)
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
        return Decorators.require_check(lambda req : is_logged_in(req.session),
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
    
    class FunctionCache:
        """
        Description
        ___________
        class that provides a cache and cache decorator for functions to cache their return values
        so that they do not need to keep getting run over and over agin, 

        inteanded for use inside of other classes


        Usage
        _____
        class SomeModel:
            def __init__(self,*args,**kwargs):
                super().__init__(*args,**kwargs)
                self.cache = FunctionCache()


            @self.cache.cashify()
            def some_costly_function():
                return long_operation()

        now some_costly_function will cache its return value


        Notes
        _____
        currently this class only supports functions where changing their arguments does not change the caching
        you could improve upon this in the future, but for our use cases this works just fine

        you could probagbly use (f,args) as the cache key and then go from there, but since this is extra work
        that would slow down development time that feature is left out for now, somthin' for version 2.0 :)


        cache entries are stored as (function,last_update_time,update_frequency) where a null update_frequency means that
        the update frequency is infinity
        """
        def __init__(self):
            #handle the importing for us
            from time import time
            self.cache = {}
            self.get_time = time
           
        """
        returns true if the given function has a value saved in the cache
        """
        def is_cached(self,f : callable,args)->bool:
            if (f,args) in self.cache:
                value, last_entry_time,update_frequency = self.cache[(f,args)]
                return update_frequency == None or self.get_time() - last_entry_time > update_frequency
            return False


        """
        actually store a value in our cache
        """
        def cache_value(self,f : callable,args,value,update_frequency)->None:
            self.cache[(f,args)] = (value,self.get_time(),update_frequency)

        """
        convinence function to apply caching to a set of functions on an object
        on creation time
        """
        def cache_function_set(self,obj : object, function_names : [str])->None:
            for name in function_names:
                obj.__dict__[name] = self.create_cached_function(f)

        """
        convinence function to use the decorator and return the given function in the cache
        """
        def create_cached_function(self,f:callable,update_frequency = None):
            return self.cachify(update_frequency)(f)    
        
        """
        Description
        ___________

        decorator that caches a given function

        Usage
        _____

        class SomeModel:
            cache = FunctionCache()
            def __init__(self,*args,**kwargs):
                super().__init__(*args,**kwargs)


            @cache.cashify(10)
            def some_costly_function():
                return long_operation()

        now some_costly_function will cache its return value
        for 10 seconds before allowing the function to run again
        """
        def cachify(self,update_frequency=None):
            def decorator(f):
                def wrapper(*args,**kwargs):
                    if self.is_cached(f,args):
                        #print("caching just saved you time :)")
                        return self.cache[(f,args)][0]
                    
                    value = f(*args,**kwargs)
                    self.cache_value(f,args,value, update_frequency)
                    
                    return value
                return wrapper
            return decorator
        
#===============Adam stuff=============#
def is_ascii(s: str) -> str:
        '''
        Description
        -----------
        Check if a given string is made up of only ASCII characters.
        
        Parameters
        ----------
        - s (str): The string which is being evaluated for ASCII only characters.
        
        Returns
        -------
        - str: An empty string ("") if the string only contains ASCII characters. Otherwise, 
        a message string is returned informing that the string contains non-ASCII characters.
        
        Example Usage
        -------------
        
        >>> is_ascii("Goodbye World!")
        ""
        >>> is_ascii("💩")
        "String contains non-ASCII characters."
        
        Authors
        -------
        Adam U. :)
        '''
        
        #Standard ASCII character set ranges from 0 to 127
        return "" if all(ord(c) < 128 for c in s) else "String contains non-ASCII characters."

def contains_sql_injection_risk(input_string: str) -> str:
    '''
    Description
    -----------
    Check if a given string contains SQL query information that could be used
    to perform as SQL injection attack.
    
    Parameters
    ----------
    - input_string (str): The string which will be evaluated for SQL tokens.
    
    Returns
    -------
    - str: An empty string ("") if the string does not contain any SQL tokens. Otherwise,
    a message string is returned informing of the possible SQL tokens within the provided
    string.
    
    Example Usage
    -------------
    
    >>> contains_sql_injection_risk("Real programmers dont comment their code")
    ""
    >>> contains_sql_injection_risk("Uh oh very stinky payload ' OR 1=1 --")
    "String contains possible SQL tokens."
    
    Authors
    -------
    Adam U. 8==D~
    '''
    
    # List of patterns to check for
    patterns = [
        r"(--|\#|\*|;|=)",
        r"(SELECT\s|INSERT\s|DELETE\s|UPDATE\s|DROP\s|EXEC\s|UNION\s|ALTER\s|CREATE\s|INDEX\s|REPLACE\s)",
        r"('|\")"
    ]
    
    # Check if any of the patterns are found in the input_string
    for pattern in patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return "String contains possible SQL tokens."  # SQL injection risk found
    
    return ""  # No SQL injection risk found


VALIDATE_REQ_BODY_ERR_MSSG = "The 'validate_request_body' \
decorator is typically only used on route callback functions \
that need one or more of its body's string values verified."

def __validate_request_body(req_callback: Callable, *body_args: str, **kwargs) -> Callable:
    '''
    Description
    -----------
    
    This is a decorator function that is used with callback routes receiveding a POST request
    and verifies the values of data keys passed in with the post request

    Example Usage
    -------------

    *see "validate_request_body" decorator below

    Authors
    -------
    Adam U.
    '''
    
    def wrapper(*args,**kwargs):
        #The calling function should have at least one argument.
        if len(args) < 1:
            raise Exception(f"Function {req_callback.__name__} has no arguments! {VALIDATE_REQ_BODY_ERR_MSSG}")
        
        #The first argument of the calling function must be an HttpRequest for it to be a route callback.
        if not isinstance(args[0], HttpRequest):
            raise Exception(f"Function {req_callback.__name__} is not a route callback! {VALIDATE_REQ_BODY_ERR_MSSG}")
        
        #The decorator must have at least one parameter given to validate.
        if len(body_args) < 1:
            raise Exception(f"No body argurments for validation were provided!")
        
        #Get the request from the calling route callback function.
        req: HttpRequest = args[0]
        
        if req.method == "POST":
            #Filter the post request's data dict with the parameters provided into the decorator
            body_dict: dict = {key:req.POST[key] for key in body_args if key in req.POST}
            err_mssg: str = ""
            
            #Validate each parameter's value
            for value in body_dict.values():
                err_mssg = is_ascii(value)
                #err_mssg = contains_sql_injection_risk(value)
                
                if err_mssg != "":
                    return bad_request_400(f"{err_mssg} | problem_string: {value}")
        
        return req_callback(*args,**kwargs)
    
    return wrapper

def validate_request_body(*args: str,**kwargs):
    '''
    Description
    -----------
    Wrapper decorator for the main validation decorator

    Parameters
    ----------

    folded string list: a parameter list of POST request data keys as strings whose values neeed to be checked

    Example Usage
    -------------

    @validate_request_body("key1", "key2")
    def route(req: HttpRequest):
        --content--

    *when the route is called, the keys' data will be validated based on conditions set in the decorator
    and will return a 400 error if the validation fails*

    
    Authors
    -------
    Adam U.
    '''
    return lambda func: __validate_request_body(func, *args,**kwargs)




