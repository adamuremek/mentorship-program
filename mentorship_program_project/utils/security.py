"""
FILE NAME: security.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED:

-------------------------------------------------------------------------------
FILE PURPOSE:
Defines our suite of security functions used throughout the project.

-------------------------------------------------------------------------------
COMMAND LINE PARAMETER LIST (In Parameter Order):
(NONE)

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NONE)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
(NONE)

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
- strPepper (str): A pepper to add to passwords to increase security

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO     WHEN     WHAT
WJL   3/14/2024  Added comments and updated everything to doc standards
"""

import bcrypt
from django.conf import settings
from typing import Callable

from base64 import b64encode,b64decode

def logout(session : dict)->bool:
    """
    Description
    -----------
    Logs out the current session

    Parameters
    ----------
    - session (dict): the session to be logged out

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - bool: The success of the log out operation

    Example Usage
    -------------
    
    >>> logout(session)
    true

    Authors
    -------
    
    """
    if is_logged_in(session):
        session["login"] = False
        return True
    return False
"""properly sets the session variable to login"""
def set_logged_in(session : dict,user : 'User')->bool:
    
    #TODO: circular imports mean that we can't use the 
    #enumerators here which is EVIL
    #probably we want this security file moved into the 
    #project to avoid that
    if not user.str_role in ['Mentor','Mentee','Admin']:
        return False

    session["login"] = True
    session["user_id"] = user.id
    return True

def is_logged_in(session : dict)->bool:
    """
    Description
    -----------
    Returns the login status of a given session

    Parameters
    ----------
    - session (dict): The session to check

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - bool: The login status of the session

    Example Usage
    -------------
    
    >>> is_logged_in(session)
    true

    Authors
    -------
    
    """
    return session["login"] if "login" in session else False

"""
convinence function to return the id of the current user from a given session id
"""
def get_user_id_from_session(session : dict)->int:
    """
    Description
    -----------
    Returns the user ID associated with a given session

    Parameters
    ----------
    - session (dict): The session to get the user ID from

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - int: The user ID associated with the session

    Example Usage
    -------------
    
    >>> get_user_id_from_session(session)
    53

    Authors
    -------
    
    """
    return session["user_id"]

def black_list(data : object, black_listed_keys : [str])->None:
    """
    Description
    -----------
    A destructive function that nulls everything in the blacklist to purge data
    for front end operations

    Parameters
    ----------
    - data (obj): The blacklist object to delete from
    - black_listed_keys ([str]): The set of keys to be deleted from data

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - None

    Example Usage
    -------------
    
    >>> black_list(a_list, [password_hashes])

    Authors
    -------
    
    """
    for key in data.__dict__:
        if key in black_listed_keys:
            data.__dict__[key] = None

def is_in_debug_mode()->bool:
    """
    Description
    -----------
    Determines whether or not the project is in debug mode

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - bool: The debug state of the project (true if in debug)

    Example Usage
    -------------
    
    >>> is_in_debug_mode()
    true

    Authors
    -------
    
    """
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
    """
    Description
    -----------
    Generates a random salt using bcrypt, but is coded in a way that any
    encryption can be used.

    Parameters
    ----------
    (None)

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - str: The generated salt

    Example Usage
    -------------
    
    >>> generate_salt()
    "asidfhg90q28rof7asd87923unb9"

    Authors
    -------
    
    """
    s = b64encode(bcrypt.gensalt())
    return s.decode("UTF-8")

def hash_password(password_plain_text : str,salt : str)->str:
    """
    Description
    -----------
    Hashes a plaintext password 

    Parameters
    ----------
    - password_plain_text (str): The plaintext password
    - salt (str): The salt to be added

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - str: The hashed password

    Example Usage
    -------------
    
    >>> hash_password("abcd1234", generate_salt())
    q849hgf8va67sdhtgvf89032etgdfc87o9dgf8o97q23f8a97g0936q2g79fg6asdb9ovfq2gb3

    Authors
    -------
    
    """
    salt_data = b64decode(salt)
    peppered_password = password_plain_text + strPepper

    #anything touching the random number generators needs to be b64 encoded
    #to properly be stored in the database
    ret_val = b64encode(
            bcrypt.hashpw(peppered_password.encode('UTF-8'),salt_data)
            ).decode('UTF-8')
    return ret_val

"""
pythonic "namespace" for the decorators contained in the security file
"""
class Decorators:
    """
    Description
    -----------
    A subclass containing decorators that apply to functions to increase
    security.

    Properties
    ----------
    (None)

    Instance Functions
    -------------------
    - require_check: Generates a decorator that will test the given function by
        the given choice, and swap out the function for alternative if it fails
        that choice.
    - require_login: Requires a user to be properly logged in before executing
        the function it's decorating
    - require_debug: Requires the program to be in debug mode to execute the
        decorated function

    Static Functions
    -------
    (None)

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    
    def require_check(check : Callable[[],bool],alternate : callable)->callable:
        """
        Description
        -----------
        Generates a decorator that will test the given function by the given
        choice and swap out the function for alternative if it fails that
        choice.

        The code for this kind of thing looks nasty, but it is SO nice to use 
        after you get pasted the cursed defs in defs.

        Parameters
        ----------
        - alternate_view (callable)): The view to go to if requirements are not
            met

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - Callable: The decorated function

        Example Usage
        -------------
        
        >>>     def invalid_login_view(req):
        >>>    ...
        >>>    ...
        >>>    ...

        >>>    @require_check(lambda req : req.session[0] ==
        >>>        'login',invalid_login_view)
        >>>    def some_view(reqs):
        >>>    ...
        >>>    ...

        NOTE: 

        While the example shows how to use this method for login systems,
        there is another decorator in this file SPECIFICALLY for that purpose
        in the form of require_logged_in. 

        It is STRONGLY encouraged to use the require_logged_in function 
        so that the login code is properly parsed.

        Authors
        -------
        
        """
        
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

    def require_login(alternate_view : Callable) -> Callable:
        """
        Description
        -----------
        Requires the user to be properly logged in to execute the decorated
        function

        Parameters
        ----------
        - alternate_view (callable)): The view to go to if requirements are not
            met

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - Callable: The decorated function

        Example Usage
        -------------
        
        >>>     def invalid_login_view(req):
        >>>    ...
        >>>    ...
        >>>    ...

        >>>    @require_login(invalid_login_view)
        >>>    def some_view(reqs):
        >>>    ...
        >>>    ...

        Authors
        -------
        
        """
        return Decorators.require_check(lambda req : is_logged_in(req.session),
                             alternate_view)

    def require_debug(alternate_view : Callable) -> Callable:
        """
        Description
        -----------
        Requires the program to be in debug mode to execute the decorated
        function

        Parameters
        ----------
        - alternate_view (callable)): The view to go to if requirements are not
            met

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - Callable: The decorated function

        Example Usage
        -------------
        
        >>>     def invalid_login_view(req):
        >>>    ...
        >>>    ...
        >>>    ...

        >>>    @require_debug(invalid_login_view)
        >>>    def some_view(reqs):
        >>>    ...
        >>>    ...

        Authors
        -------
        
        """
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




