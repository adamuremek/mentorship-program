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

def set_logged_in(session : dict,user_id : int)->bool:
    """
    Description
    -----------
    Sets a user's session as signed in.

    Parameters
    ----------
    - session (dict): The session to be logged out
    - user_id (int): The session owner's user id

    Optional Parameters
    -------------------
    (None)

    Returns
    -------
    - bool: The success of the log in operation

    Example Usage
    -------------
    
    >>> set_logged_out(session, 53)
    true

    Authors
    -------
    
    """
    session["login"] = True
    session["user_id"] = user_id

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
