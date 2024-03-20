"""
FILE NAME: models.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED:

-------------------------------------------------------------------------------
FILE PURPOSE:
Defines all models to store object into the database. Every class is a data-
access object.

-------------------------------------------------------------------------------
COMMAND LINE PARAMETER LIST (In Parameter Order):
(NONE)

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NOTHING)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
from  mentorship_program_app.models import *
User.objects.create(...)

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
(NONE)

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO   WHEN     WHAT
WJL  2/26/24   Added file header comment and began commenting functions
WJL   3/1/24   Finished adding comments to this file
WJL   3/3/24   Fully fixed and finished updating documentation on this file
"""

#django imports
from django.conf import settings
from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.http import HttpResponse,HttpRequest # for typing



#standard python imports
from datetime import date
import os
from typing import Callable
import random
import string
from enum import Enum


#project imports
from utils import security
from django.utils import timezone
from datetime import timedelta
from typing import Tuple


# Create your models here.

"""
class containing functions we want in every one of our 
models, but not necessarily model classes
"""
class SVSUModelData():
    """
    Description
    -----------
    A class containing functions we want in every one
    of our models, but not necessarily model classes.

    Properties
    ----------
    (None)

    Instance Functions
    -------------------
    - sanitize_black_properties: Sets all read-only properties
        in the blacklist to None

    Static Functions
    -------
    - get_backend_only_properties:
        Returns a string list of properties only for back-end technologies

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    #ensure that this model is not stored in the database
    #it is ONLY a logical model
    abstract = True

    @staticmethod
    def get_backend_only_properties()->[str]:
        """
        Description
        -----------
        Get a static list of properties to be hidden from front-end technologies

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - [str]: A list containing the properties as strings

        Example Usage
        -------------

        >>> SVSUModelData.get_backend_only_properties()
        '["save", "delete"]'

        Authors
        -------
        
        """
        return ["save","delete"]
    

    def sanitize_black_properties(self, black_list : list[str] = []) -> 'SVSUModelData':
        """
        Description
        -----------
        Sets all read-only properties in the blacklist to None

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        - black_list ([str]): The list of properties on the blacklist.

        Returns
        -------
        - SVSUModelData: Returns itself for convenience.

        Example Usage
        -------------

        >>> svsu_data_model.sanititze_black_properties()
        'svsu_data_model'

        Authors
        -------
        
        """
        security.black_list(self,self.get_backend_only_properties() + black_list)
        return self




class Interest(SVSUModelData,Model):
    """
    Description
    -----------
    A class outlining the model for user interests

    Properties
    ----------
    - strInterest - descriptive text regaurding what this interest is
    - isDefaultInterest - is true only if we added the initial interest at the start of the app, false for user defined interests

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    - get_default_interests: Returns a list of the default interests
    - get_initial_default_interest_strings: Returns a string list of hard-coded
        default interest strings

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    strInterest = CharField(max_length=100, null=False,unique=True)
    isDefaultInterest = BooleanField(default=False)


    @staticmethod
    def create_interest(str_interest : str, bool_default : bool = False) -> 'Interest' :
        """
        Description
        -----------
        Creates an interest given a name and boolean value to determine 
        if the interest is a default interest.


        Example Usage
        _____________
        >>> my_interest = create_interest("Computer Science")


        Authors
        -------
        Justin Goupil
        """
        #Create the interest and save it to the database in one line.
        try:
            return Interest.objects.create(
                strInterest = str_interest,
                isDefaultInterest = bool_default
            )
        except :
            return None
        
    
    @staticmethod
    def get_interest(str_interest_name : str ) -> 'Interest' :
        """
        Description
        -----------
        Gets an interest by name.


        Example Usage
        _____________
        >>> my_interest = get_interest("Computer Science")


        Authors
        -------
        Justin Goupil
        """
        
        try:
            #Find the first instance of the interest in the database and return the object.
            return Interest.objects.filter(str_interest = str_interest_name).first()
        except:
            return None
    
    @staticmethod
    def update_interest(str_interest_name : str, bool_default : bool, str_new_interest_name : str = None) -> 'Interest' :
        """
        Description
        -----------
        Updates an interest with a new default value or interest name.


        Example Usage
        _____________
        >>> my_interest = update_interest("Netwoking", True, "Networking")


        Authors
        -------
        Justin Goupil
        """
        try:
            #Find the first instance of the interest in the database and return the object.
            interest : 'Interest' = Interest.objects.filter(str_interest = str_interest_name)
            
            if str_new_interest_name != None :
                interest.strInterest = str_new_interest_name
            
            interest.isDefaultInterest = bool_default

            #save the instance to the database
            interest.save()

            return interest
        except:
            return None
    
    @staticmethod
    def delete_interest(str_interest_name : str) -> 'Interest' :
        """
        Description
        -----------
        Removes an interest from the database.


        Example Usage
        _____________
        >>> my_interest = delete_interest("Compter Science")


        Authors
        -------
        Justin Goupil
        """
        try:
            #Find the first instance of the interest in the database and return the object.
            interest : 'Interest' = Interest.objects.filter(str_interest = str_interest_name)
            interest.delete()

            return interest
        except:
            return None

    @staticmethod
    def get_or_create_interest(str_interest : str) -> 'Interest':
        """
        Description
        -----------
        attempts to get a given interest, if it does not exist in the db create it


        Example Usage
        _____________
        my_interest = Interest.get_or_create_interest("Buffalo Breeding")


        Authors
        -------
        David Kennamer )-(
        """
        try:
            ret_int = Interest.objects.get(strInterest = str_interest)
            return ret_int
        except ObjectDoesNotExist:
            #TODO: put in try catch to account for connection issues
            Interest.objects.create(strInterest=str_interest).save()


    #convinence methods
    @staticmethod
    def get_default_interests() -> QuerySet:
        """
        Description
        -----------
        Returns a list of all default interest objects

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - QuerySet: The set of all default interest objects

        Example Usage
        -------------

        >>> Interest.get_default_interests()
        '<[Interest: c++, Interest: python, Interest: html, ...]>'

        Authors
        -------
        
        """
        return Interest.objects.filter(isDefaultInterest=True)

    # def __str__(self) -> str:
    #     return self.strInterest

class User(SVSUModelData,Model):
    """
    Description
    -----------
    A class outlining the model for users

    Properties
    ----------
    - cls_email_address
    - str_password_hash
    - str_password_salt
    - str_role
    - cls_date_joined
    - cls_active_changed_date
    - bln_active
    - bln_account_disabled
    - str_first_name
    - str_last_name
    - str_phone_number
    - str_last_login_date
    - str_gender
    - str_preferred_pronouns
    - interests

    Instance Functions
    -------------------
    - get_backend_only_properties:
        Returns a string list of properties only for back-end technologies
    - is_mentor: Returns true if the user is a mentor
    - is_mentee: Returns true if the user is a mentee
    - check_valid_password: Returns true if the entered
        password matches the store password
    - get_user_info: Returns a dictionary of the user's information

    Static Functions
    -------
    - create_from_plain_text_and_email: Creates a new user object
    - from_session: Gets a user object using a session
    - check_valid_login: Checks if a given email/pass combination is correct

    Magic Functions
    -------------
    (None)

    Authors
    -------

    """

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) #let django cook
        
        #mark cached functions so we don't over query the database
        self.cache = security.Decorators.FunctionCache()
        
        #decorate cachable functions on the init level so python understands when to remove
        #the cached data
        self.is_mentee = self.cache.create_cached_function(self.is_mentee)
        self.is_mentor = self.cache.create_cached_function(self.is_mentor)



    @property 
    def str_full_name(self):
        first_name = self.str_first_name if self.str_first_name != None else " "
        last_name =  self.str_last_name if self.str_last_name != None else " "
        return first_name + " " + last_name

    def get_recomended_users(self):
        """
        Description
        ___________
        query that returns opposite users in the database that are ordered base on their 
        interest similarity to the current user

        Notes
        _____
        the idea here is to keep the number crunching as much on the databse side of things as possible
        so the query first computes your likely score to the current user on the db in a subquery, 
        and then uses that to order on after the sub query finishes

        Authors
        _______
        David Kennamer >.>
        """

        return User.objects.raw(
                    f"""
                    SELECT DISTINCT t1.user_id AS id,str_first_name,str_last_name,COUNT(*) as likeness
                       FROM mentorship_program_app_user_interests AS t1, mentorship_program_app_user_interests AS t2,mentorship_program_app_user AS tu
                       WHERE t2.user_id={self.id} AND t1.interest_id = t2.interest_id AND t1.user_id = tu.id
                             AND tu.str_role = '{self.get_opposite_database_role_string()}'
                       GROUP BY t1.user_id,tu.str_first_name,tu.str_last_name
                       ORDER BY likeness DESC;
                    """
                    )

        
        #quick and dirty method
        #pings the database a lil' more than I would like
        #this method fails to work properly since it does not accout for every item in the database
        #due to pagination from django, we need this query to run on the server
        
        #q_obj = User.objects.filter(str_role=self.get_opposite_database_role_string())
        #ret_val =  []
        #for u in q_obj:
        #    u.likeness = float((u.interests.all() & self.interests.all()).count())
        #    ret_val.append(u)
        #ret_val.sort(key = lambda x : x.likeness,reverse=True)

        #ret_val = ret_val


        #return ret_val


    def get_backend_only_properties(self)-> list[str]:
        """
        Description
        -----------
        Get a list of properties to be hidden from front-end technologies
        overrides from SVSUModelData

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - [str]: A list containing the properties as strings

        Example Usage
        -------------

        >>> User.get_backend_only_properties()
        '["save", "delete", "str_password_hash", "str_password_salt", "check_valid_passowrd"]'

        Authors
        -------
        
        """
        return super().get_backend_only_properties() + [
                "str_password_hash",
                "str_password_salt",
                "check_valid_password"
                ]
    
    class ErrorCode:
        AlreadySelectedEmail = -1

    class Role(TextChoices):
        """
        Description
        -----------
        An enum subclass to hold the different user roles

        Properties
        ----------
        - ADMIN
        - MENTOR
        - MENTEE
        - MENTOR_PENDING
        - GRADUATED
        - DECLINED

        Instance Functions
        -------------------
        (None)

        Static Functions
        -------
        (None)

        Magic Functions
        -------------
        (None)

        Authors
        -------
        
        """
        ADMIN = 'Admin'
        MENTOR = 'Mentor'
        MENTEE = 'Mentee'
        MENTOR_PENDING = 'MentorPending'
        GRADUATED = 'Graduated'
        DECLINED = 'Declined'

    cls_email_address =  EmailField(null=True,unique=True)  
    str_password_hash =  CharField(max_length=1000, null=True, blank=False)
    str_password_salt =  CharField(max_length=1000, null=True, blank=False)
    str_role = CharField(max_length=15, choices=Role.choices, default='')
    cls_date_joined = DateField(default=date.today)
    cls_active_changed_date = DateField(default=date.today)
    bln_active = BooleanField(default=True)
    bln_account_disabled =  BooleanField(default=False)

    str_first_name : CharField =  CharField(max_length=747,null=True)
    str_last_name : CharField =  CharField(max_length=747, null=True) 
    str_phone_number : CharField = CharField(max_length=15, null=True)
    str_last_login_date = DateField(default=date.today)
    str_gender = CharField(max_length=35, default='')
    str_preferred_pronouns = CharField(max_length=50, null=True)
    str_bio = CharField(max_length=5000, default='')
    #foregn key fields
    interests = models.ManyToManyField(Interest)
        
    def has_requested_user(self,other_user_id : int)->'MentorshipRequest':
        """
        Description
        -----------
        returns true if the given user has a MentorShipRequest with the other user

        Parameters
        ----------
        other : User - the other use we want to see if we have a mentorship relation with

        Returns
        -------
        - MentorshipRequest if it exists, otherwise None


        Example Usage
        -------------

        >>> some_user.has_requested_user(other_user)
        MentorShipRequest of the users or False if it doesn't exist

        Authors
        -------
        David Kennamer ~.~
        Tanner 🦞
        """
        try:
            if self.is_mentor():
                return MentorshipRequest.objects.get(mentor=self,mentee_id=other_user_id) 
            return MentorshipRequest.objects.get(mentee=self,mentor_id=other_user_id ) 
        except:
            return False


    def get_opposite_database_role_string(self)->str:
        """
        Description
        -----------
        returns a string representing the opposite role based on existence in the database

        convinence function

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - str: Mentor if mentor esle MEntee
        read the python :p ^

        Example Usage
        -------------

        >>> user_joe.get_database_role_str()
        'Mentor'

        Authors
        -------
        
        """

        return User.Role.MENTEE if  self.is_mentor()  else User.Role.MENTOR

    def get_database_role_string(self)->str:
        """
        Description
        -----------
        returns a string representing the state of the database based on if 
        the database is a mentor

        convinence function

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - str: Mentor if mentor else MEntee
        read the python :p ^

        Example Usage
        -------------

        >>> user_joe.get_database_role_str()
        'Mentor'

        Authors
        -------
        David Kennamer ._.
        Jordan Anodjo
        
        """
        
        return User.Role.MENTOR if self.is_mentor()  else User.Role.MENTEE


    def is_mentor(self)->bool:
        """
        Description
        -----------
        Returns whether the current user is a mentor

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - bool: Is the user a mentor

        Example Usage
        -------------

        >>> user_joe.is_mentor()
        true

        Authors
        -------
        
        """
        try:
            self.mentor
            return self.str_role == User.Role.MENTOR
        except ObjectDoesNotExist:
            return False

    def is_mentee(self)->bool:
        """
        Description
        -----------
        Returns whether the current user is a mentee

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - bool: Is the user a mentee

        Example Usage
        -------------

        >>> user_joe.is_mentee()
        false

        Authors
        -------
        
        """
        try:
            self.mentee
            return self.str_role == User.Role.MENTEE
        except ObjectDoesNotExist:
            return False
    
    def is_super_admin(self)->bool:
        """
        convinece function that returns true if the given user has super admin privleges in the database
        """
        try:
            return  self.str_role == "Admin" or self.admin_entry.bool_enabled
        except ObjectDoesNotExist:
            
            return False

    def get_shared_organizations(self,other : 'User')->['Organization']:
        """
        returns a set of organizations that the two given users share
        """
        #only mentors have organizations
        if not (self.is_mentor() and other.is_mentor()): return None

        return self.mentor.organizations & other.mentor.organizations




    def get_first_shared_organization(self,other : 'User')->'Organization':
        """
        returns the first shared organization if it exists, otherwise None
        """
        #mentees do not have an organization
        if self.is_mentee() or other.is_mentee(): return None
        
        my_organizations =  self.mentor.organizations.all()
        your_organizations =  [o.id for o in other.mentor.organizations.all()]

        #get the intersection of the id's
        #realistically users will only be a part of one to two organiazitons
        for my_org in my_organizations:
            if my_org.id in your_organizations:
                return my_org
        return None

    def has_authority(self, other : 'User')->bool:
        """
        returns true if the given user account has authority over the second user account
        """
        if self.id == other.id: return True
        if self.is_super_admin(): return True
        
        if self.is_mentor() and other.is_mentor():
            #if we are both mentors, check if we share an organization

            shared_organizations = self.mentor.get_shared_organizations(other.mentor)

            for org in shared_organizations:
                if self.mentor.is_admin_of_organization(org):
                    return True
        
        return False



    
    def check_valid_password(self,password_plain_text : str)->bool:
        """
        Description
        -----------
        Checks whether the incoming password matches the stored password

        Parameters
        ----------
        - password_plain_text (str): The incoming password plaintext

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - bool: Do the passwords match

        Example Usage
        -------------

        >>> user_joe.check_valid_password("password")
        true

        Authors
        -------
        
        """
        return security.hash_password(password_plain_text,self.str_password_hash) ==\
                self.str_password_hash


    def create_mentorship_from_user_ids(self,mentee_user_account_id : int,mentor_user_acount_id : int)->tuple['User','User']:
        """
        Description
        ___________
        convinence function that creates a relationship between a mentor and a mentee given their account id's

        returns a tuple of the accounts from the database for further processing, will fail if the user this is running from
        does NOT have permission to interact with the database

        Returns
        _______
        a tuple of user objects where the first object is the mentee and the second the mentor

        if you do not have permission to create the request, it returns (None,None)

        Authors
        _______
        David Kennamer <.<
        """
        
        #ensure that the person creating the request is a mentor (also admin, since admin is a subset of mentor)
        # if not self.is_mentor():
        #     return (None,None)

        mentor_user_account = User.objects.get(id=mentor_user_acount_id)

        if mentor_user_account.mentor.has_maxed_mentees():
            raise ValidationError('mentor has max mentees!')
            return (None,None)
    
        # if not self.has_authority(mentor_user_account):
        #     return (None,None)

        mentee_user_account = User.objects.get(id=mentee_user_account_id)
        mentee_account = mentee_user_account.mentee
        mentee_account.mentor = mentor_user_account.mentor
        mentee_account.save()

        #make sure to remove all MentorShipRequests that are in the database still, since this mentee now has a mentor
        MentorshipRequest.remove_all_from_mentee(mentee_account)

        # record logs
        # record the mentee since the mentor can be gathered from it later
        SystemLogs.objects.create(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT, 
                                  specified_user= User.objects.get(id=mentee_user_account_id))

        return (mentee_account,mentee_account.mentor)

    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'User':
        """
        Description
        -----------
        Creates a user object WITHOUT saving it to the database. Author note:
        it's your responsibility to save this object 
        if you want it to persist in the db YOU HAVE BEEN WARNED >_>

        Parameters
        ----------
        - password_plain_text (str): The user's password as plaintext
        - email (str): The user's email

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - User: the created user object on sucesful
        - -1 if email already exists

        Example Usage
        -------------

        >>> User.create_from_plain_text_and_email("password", "joeshmo@email.com")
        NewUserObject1

        Authors
        -------
        
        """

        if User.objects.filter(cls_email_address=email).count() != 0:    
            return User.ErrorCode.AlreadySelectedEmail

        generated_user_salt = security.generate_salt()
        #TODO: emails need to be validated, send a sacrifical lamb
        #to the regex gods
        return User.objects.create(
                    str_password_hash = security.hash_password(
                                            password_plain_text,
                                            generated_user_salt),
                    str_password_salt = generated_user_salt,
                    cls_email_address = email
                )

    @staticmethod 
    def from_session(session)->'User':
        """
        Description
        -----------
        Returns a user object based on the session data
        Requires the user to be logged in

        Parameters
        ----------
        - session (dict): The session

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - User: The user object for the logged in user
        - None: The user is not logged in

        Example Usage
        -------------

        >>> User.from_session(req.session)
        NewUserObject2

        Authors
        -------
        
        """
        if not security.is_logged_in(session): return None

        return User.objects.get(id=session.get("user_id"))

    @staticmethod
    def check_valid_login(str_email:str, str_password_plain_text:str):
        """
        Description
        -----------
        Returns whether the given email/password combination is correct

        Parameters
        ----------
        - str_email (str): The entered email
        - str_password_plain_text (str): The entered password

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - bool: The result of the login check

        Example Usage
        -------------

        >>> User.check_valid_login("joeshmo@email.com", "password")
        true

        Authors
        -------
        
        """
        try:
            u = User.objects.get(cls_email_address=str_email)
        except ObjectDoesNotExist:
            return False
        return u.check_valid_password(str_password_plain_text)

    def get_user_info(self) -> dict:
        """
        Description
        -----------
        Returns a dictionary of the user information

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - dict: The user's information

        Example Usage
        -------------

        >>> user_joe.get_user_info()
        {
        "EmailAddress":"joeshmo@email.com",
        "Role":"Mentor",
        "DateJoined":3/1/2024,
        ...
        }

        Authors
        -------
        
        """
        user_info = {
            "EmailAddress": self.cls_email_address,
            "Role": self.str_role,
            "DateJoined": self.cls_date_joined,
            "ActiveChangedDate": self.cls_active_changed_date,
            "Active": self.bln_active,
            "AccountDisabled": self.bln_account_disabled,
            "FirstName": self.str_first_name,
            "LastName": self.str_last_name,
            "PhoneNumber": self.str_phone_number,
            "DateOfBirth": self.cls_date_of_birth,
            "Gender": self.str_gender,
            "PreferredPronouns": self.str_preferred_pronouns,
            "str_bio" : self.str_bio
        }



        return user_info
    
    # @property
    # def img_user_profile(self):
    #     """
    #     DESCRIPTION
    #     ___________

    #     convinence property to provide access to the users profile image through
    #     the original user.img_user_profile api for the sake of views and ensuring images
    #     still work with the older api method

    #     see https://realpython.com/python-property/ 
    #     for a reference on how python properties work

    #     USAGE
    #     _____
        
    #     in django

    #     django_img_field = user.img_user_profile

    #     in a view
        
    #     <img class="card-profile-image" src="{{ user.img_user_profile.url }}"/>

    #     AUTHORS
    #     _______
    #     David Kennamer ._.

    #     """
    #     try:
    #         default_img = self.profileimg.img_profile
    #     except ObjectDoesNotExist:
    #         ProfileImg.create_from_user_id(self.id) #create an image with default profile picture if one does not exist
    #     return self.profileimg.img_profile
    
    @property
    def profile_img(self):
        """
        DESCRIPTION
        ___________

        convinence property to provide access to the users profile image through
        the original user.profile_img api for the sake of views and ensuring images
        still work with the older api method

        see https://realpython.com/python-property/ 
        for a reference on how python properties work

        USAGE
        _____
        
        in django

        django_img_field = user.profile_img

        in a view
        
        <img class="card-profile-image" src="{{ user.profile_img.img.url }}"/>

        AUTHORS
        _______
        David Kennamer ._0
        Adam U. <:3
        """
        try:
            return self.profile_img_query
        except ObjectDoesNotExist:
            img = ProfileImg.create_from_user_id(self.id)
            return img

    @property
    def cleaned_bio(self) -> str:
        """
        DESCRIPTION
        ===========

        By default, the "str_bio" model property, which is a CharField, returns a string
        padded with spaces and carriage returns. This property wrapper (getter) just returns
        a cleaned form of that string.

        USAGE
        =====
        
        >>> print(user.str_bio)
        "         This is my Bio\n\r         "

        >>> print(user.cleaned_bio)
        "This is my bio"
        
        Author
        ======
        Adam U. >:3
        """
        
        return self.str_bio.strip()

    class Decorators:
        """
        Description
        -----------
        A subclass containing decorators that apply to views SPECIFICALLY
        to limit the kind of user that can interact with the view. We would
        prefer these in the security file, but since that will cause a circular
        dependency, and these have to do entierly with users it makes sense
        to place them here.

        Properties
        ----------
        (None)

        Instance Functions
        -------------------
        (None)

        Static Functions
        -------
        - require_logged_in_mentor: Prevents users who aren't logged in as a
            mentor from accessing certain pages
        - require_logged_in_mentee: Prevents users who aren't logged in as a
            mentee from accessing certain pages
        - require_logged_in_super_admin: Prevents users who aren't logged in as
            a super admin from accessing certain pages

        Magic Functions
        -------------
        (None)

        Authors
        -------
        
        """
        @staticmethod
        def require_logged_in_mentor(alternate_view : Callable): # -> Callable[HttpRequest,HttpResponse]:
            """
            Description
            -----------
            Prevents users who aren't logged in as a mentor from accessing
            certain pages

            Parameters
            ----------
            - alternate_view (Any): The page to redirect to if the user logged
                in is not a mentor

            Optional Parameters
            -------------------
            (None)

            Returns
            -------
            - Any: The decorated function with the redirect

            Example Usage
            -------------
            def some_other_view(req : HttpRequest)->HttpResponse:
                ...

            @Users.require_logged_in_mentor(some_other_view)
            def protected_view(req : HttpRequest)->HttpResponse

            Authors
            -------
            David Kennamer ._.
            """
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_mentor()
            return security.Decorators.require_check(validator, alternate_view)
        
        @staticmethod
        def require_logged_in_mentee(alternate_view : Callable): # -> Callable[HttpRequest,HttpResponse]:
            """
            Description
            -----------
            Prevents users who aren't logged in as a mentee from accessing
            certain pages

            Parameters
            ----------
            - alternate_view (Any): The page to redirect to if the user logged
                in is not a mentor

            Optional Parameters
            -------------------
            (None)

            Returns
            -------
            - Any: The decorated function with the redirect

            Example Usage
            -------------
            def some_other_view(req : HttpRequest)->HttpResponse:
                ...

            @Users.require_logged_in_mentee(some_other_view)
            def protected_view(req : HttpRequest)->HttpResponse

            Authors
            -------
            David Kennamer >.<
            """
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_mentee()
            return security.Decorators.require_check(validator, alternate_view)
        
        @staticmethod
        def require_logged_in_super_admin(alternate_view : Callable): # -> Callable[HttpRequest,HttpResponse]:
            """
            Description
            -----------
            Prevents users who aren't logged in as a super admin from accessing
            certain pages or performing certain operations

            Parameters
            ----------
            - alternate_view (Any): The page to redirect to if the user logged
                in is not a mentor

            Optional Parameters
            -------------------
            (None)

            Returns
            -------
            - Any: The decorated function with the redirect

            Example Usage
            -------------
            def some_other_view(req : HttpRequest)->HttpResponse:
                ...

            @Users.require_logged_in_super_admin(some_other_view)
            def protected_view(req : HttpRequest)->HttpResponse

            Authors
            -------
            David Kennamer
            William Lipscom:b
            NOTE: I basically just ctrl c + ctrl v from above.
            """
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_super_admin()
            return security.Decorators.require_check(validator, alternate_view)



class SuperAdminEntry(SVSUModelData,Model):
    """
    this class represents a list of super admin mentors in the database

    if you have an entry in this table you are super admin,
    if you do not have an entry, you are not super admin
    """
    bool_enabled = BooleanField(default=True) #can be used to turn off admin
    user_account = OneToOneField(User, on_delete=models.CASCADE,related_name="admin_entry")


class Organization(SVSUModelData,Model):
    """
    Description
    -----------
    A class to store information about an organization.

    Properties
    ----------
    - str_org_name (str): The name of the organization
    - str_industry_type (str): The industry the organization operate in

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    (None)

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    str_org_name = CharField(max_length=100)
    str_industry_type = CharField(max_length=100)

    admins = models.ManyToManyField('Mentor',related_name='administered_organizations') 

class Mentor(SVSUModelData,Model):
    """
    Description
    -----------
    A class that specifies a user as a mentor and provides mentor-specific
    properties.

    Properties
    ----------
    - int_max_mentees (int): The most mentees that can be assigned to this
        mentor at any given time
    - int_recommendations (int): The number of recommendations this mentor has
        received
    - str_job_title (str): The mentor's official job title
    - account (User): The base user account

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    - create_from_plain_text_and_email: Creates a mentor object and saves it to
        the database. Utilizes the existing User.create_from... method.

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """

    def has_maxed_mentees(self)->bool:
        """
        Description
        ___________
        returns true if the given mentor has maxed mentees
        """
        return self._mentee_set.count() >= self.int_max_mentees
    
    @property
    def mentee_set(self):
        """
        Description
        ___________
        read only property that ensures mentors do not get more mentees
        """
        
        def wrapper(*args,**kwargs):
            if self.has_maxed_mentees():
                raise ValidationError('mentor has maxed mentees!')
            return self._mentee_set.add(*args,**kwargs)
        
        self._mentee_set.add = wrapper

        return self._mentee_set




    def is_admin_of_organization(self,org : 'Organization')->bool:
        """
        returns true if the given user administers the given organization
        """
        try:
            org.admins.get(id=self.id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_shared_organizations(self,other : 'Mentor')->['Organization']:
        """
        returns a list of organizations shared between two mentors,
        the list will be empty if no mentors exists
        """
        return self.organizations.all() & other.organizations.all()
        
    int_max_mentees = IntegerField(default=4)
   
    # TODO:
    # I think theres a way to make this a read only query to the db
    # which is what it prolly should be so our data states
    # don't get de synced
    # -dk
    #int_recommendations = IntegerField(default=0)

    str_job_title = CharField(max_length=100)
    str_experience = CharField(max_length=50, default='')


    account = OneToOneField(
        User,
        on_delete = models.CASCADE
    )


    organization = ManyToManyField(
        Organization
    )

    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'Mentor':

        """
        Description
        -----------
        Creates a mentor object using a given email and password and saves it
        to the database

        Parameters
        ----------
        - password_plain_text: The unhashed password
        - email: The email

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - Mentor: The newly created mentor object

        Example Usage
        -------------
        
        >>> Mentor.create_from_plain_text_and_email("password",
                "smartguy@email.com") MentorObjectInstance1

        Authors
        -------
        
        """
        user_model = User.create_from_plain_text_and_email(password_plain_text,email)

        #pass the error codes through to the outside
        if type(user_model) == int:
            return user_model

        user_model.str_role = User.Role.MENTOR_PENDING
        
        #user_model.save()

        mentor = Mentor.objects.create(account=user_model)
        mentor.save()
        return mentor

class Mentee(SVSUModelData,Model):
    """
    Description
    -----------
    A class that specifies a user as a mentee.

    Properties
    ----------
    (None)

    Instance Functions
    ------------------
    (None)

    Static Functions
    ----------------
    - create_from_plain_text_and_email: Creates a mentee object and saves it to
        the database. Utilizes the existing User.create_from... method.

    Magic Functions
    ---------------
    (None)

    Authors
    -------

    """

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.function_cache = security.Decorators.FunctionCache()
        self.has_maxed_request_count = self.function_cache.create_cached_function(self.has_maxed_request_count)


    #limits the number of requests that any given mentee can have
    MAXIMUM_REQUEST_COUNT = 5

    account = OneToOneField(
        "User",
        on_delete = models.CASCADE
    )
    mentor = models.ForeignKey('Mentor',
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='_mentee_set',
                                db_column="mentor_id")

    #TODO: figure out why the heck these don't work >.<
    #@property
    #def mentor(self):
    #    print("hello from the mentor property")
    #    return self._mentor
    #@mentor.setter
    #def mentor(self,val : 'Mentor'):
    #    if val != None and val.id != self._mentor.id and val.has_maxed_mentees():
    #        raise ValidationError('mentor has maxed mentees!')

    #    self._mentor = val


    @staticmethod
    def mentee_has_maxed_request_count(mentee_account_id : int)->bool:
        """
        simple function that returns true if a given mentee has more mentors than the maximum request count
        """
        try:
            return MentorshipRequest.objects.filter(requester=mentee_account_id).count() >= Mentee.MAXIMUM_REQUEST_COUNT
        except ObjectDoesNotExist:
            return False

    def has_maxed_request_count(self)->bool:
        """
        syntactic sugar function that returns true if the given mentee has maxed their request count
        """
        return Mentee.mentee_has_maxed_request_count(self.account.id)
    
    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'Mentee':
        """
        Description
        -----------
        Creates a mentee object using a given email and password and saves it
        to the database

        Parameters
        ----------
        - password_plain_text: The unhashed password
        - email: The email

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - Mentee: The newly created mentee object

        Example Usage
        -------------
        
        >>> Mentee.create_from_plain_text_and_email("password",
                "studentname@email.edu")
        MenteeObjectInstance1

        Authors
        -------
        
        """
        user_model = User.create_from_plain_text_and_email(password_plain_text,email)

        #pass the error codes through to the outside
        if type(user_model) == int:
            return user_model

        user_model.str_role = User.Role.MENTEE
        user_model.save()

        mentee = Mentee.objects.create(account=user_model)
        mentee.save()
        return mentee


class MentorshipRequest(SVSUModelData,Model):
    """
    Description
    -----------
    MentorshipRequest is a database access object. 
    This class represents the mentorship relation 
    between a mentor and mentee.

    Properties
    ----------
    - mentor (ForeignKey): Represents a user who is a mentor.
    - mentee (ForeignKey): Represents a user who is a mentee.

    Instance Functions
    ------------------
    - create_request: Creates a request in the database using two user IDs.
    - get_request_id: Returns a specified request using an ID.
    - get_request_info: Returns a dictionary containing the fields of the request.
    - remove_request: Removes an entry from the database using two user IDs.

    Static Functions
    ----------------
    - NONE -

    Magic Functions
    ---------------
    - NONE -

    Authors
    -------
    Justin G.
    """

    mentor = ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "mentor_to_mentee_set"
        
    )
    mentee = ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "mentee_to_mentor_set"
    )

    requester = IntegerField(null=True)

    def accept_request(self,session_user : User)->bool:
        """
        Description
        ___________
        accepts the given mentorship request


        fails if the given session user does NOT have PERMISSION to make the request

        Authors
        _______
        David Kennamer *_*
        Tanner Williams 🦞
        """

        # record logs
        # record the mentee since the mentor can be gathered from it later
        mentor,mentee = session_user.create_mentorship_from_user_ids(
                                                    self.mentee.id,
                                                    self.mentor.id
                                                    )
        print(mentor, mentee)
        if mentor == None or mentee == None:
            
            return False

        SystemLogs.objects.create(str_event=SystemLogs.Event.APPROVE_MENTORSHIP_EVENT,
                                  specified_user=mentee.account)

       
        MentorshipRequest.remove_all_from_mentee(mentee)
        print("AHH GOOD")
        return True
        

    def remove_all_from_mentee(mentee : 'Mentee')->None:
        """
        Description
        ___________
        convinence function that removes all mentorship requests from the database that match a given mentee

        Authors
        _______
        David Kennamer \*^*/
        """
        MentorshipRequest.objects.filter(mentee=mentee.account).delete()

    def is_accepted(self)->bool:
        """
        Description
        ___________
        returns true if the given request is accepted in the database, ideally this should 
        allways be false, since we delete mentorship requests when we add them to a user

        this is here as an extra security check to make sure that the request is NOT accepted
        if this ever returns true it indicates invalid data

        Authors
        _______
        David Kennamer ).)
        Tanner Williams 🦞
        """
        try:
            self.mentor.mentees.get(id=self.mentee.id)
            return True
        except:
            return False


    
    @staticmethod
    def create_request(int_mentor_user_id: int, int_mentee_user_id: int, requester_id: int):
        """
        Description
        -----------
        Creates a mentorship request using two user ids.

        Parameters
        ----------
        - int_mentor_user_id (int): User ID that is the mentor.
        - int_mentee_user_id (int): User ID that is the mentee.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - True (boolean): IF the mentorship request was sucessfully created.
        - False (boolean): IF the mentorship request was NOT created.

        Example Usage
        -------------
        >>> boolFlag = create_request(13, 16)
        boolFlag = False
        >>> boolFlag = create_request(5, 24)
        boolFlag = True

        Authors
        -------
        Justin G.

        Changes
        -------
        David Kennamer 0-0 - returns request as object for saving
        """

        try:
            #prevent requests for mentors that have their mentee count maxed
            mentor_user_account = User.objects.get(id=int_mentor_user_id)
            if mentor_user_account.mentor.has_maxed_mentees():
                return False

            mentee_user_account = User.objects.get(id=int_mentee_user_id)
            if mentee_user_account.mentee.has_maxed_request_count():
                return False

            mentor_ship_request = MentorshipRequest.objects.create(
                mentor_id = int_mentor_user_id,
                mentee_id = int_mentee_user_id,
                requester = requester_id
            )
            return mentor_ship_request
        except Exception as e:
            print(e)
            return False

    def get_request_id(int_request_id: int) -> 'MentorshipRequest':
        """
        Description
        -----------
        - Gets a MentorshipRequest object specified by it's ID.

        Parameters
        ----------
        -int_request_id (int): An intiger specifying an object in the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - A MentorshipRequest object.
        - Nothing if the requested MentorshipRequest object does not exist.

        Example Usage
        -------------
        >>> cls_request = get_request_id()
        cls_request.mentee = 7
        cls_request.mentor = 8

        Authors
        -------
        Justin G.
        """
        return MentorshipRequest.objects.get(id = int_request_id)


    def get_request_info(int_request_id: int) -> dict:
        """
        Description
        -----------
        - Gets a specified MentorshipRequest by it's ID.
        - Returns a dictionary containing the user ID of the mentor and mentee.

        Parameters
        ----------
        - int_request_id (int): Integer specifying the id of a MentorshipRequest in
            the database.
        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - dict_request (Dictionary, String): Containing mentorID and menteeID.
        Example Usage
        -------------
        >>> dict_request = get_request_id(5)
        dict_request = {'mentorID': 1, 'menteeID': 2}

        Authors
        -------
        Justin G.
        """

        cls_request =  MentorshipRequest.get_request_id(int_request_id)

        dict_request = {
            "mentor_ID" : cls_request.mentor_id,
            "mentee_ID" : cls_request.mentee_id
        }

        return dict_request
    
    def remove_request(int_mentor_id: int, int_mentee_id: int) -> bool:
        """
        Description
        -----------
        Removes a mentorship request from the database.

        Parameters
        ----------
        - int_mentor_id: (int):
        - int_mentee_id: (int):



            Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - True: IF the MentorshipRequest was removed from the database.
        - False IF the MentorshipRequest was NOT removed from the database.
        
        Example Usage
        -------------
        >>> boolFlag = remove_request(25, 19)
        boolFlag = True
        >>> boolFlag = remove_request(45, 75)
        boolFlag = False

        Authors
        -------
        Justin G.
        """
        try:
            MentorshipRequest.objects.filter(mentor = int_mentor_id, mentee = int_mentee_id).delete()
            return True
        except Exception as e:
            return False

    class Meta:
        """
        Description
        ___________

        django provides the capabilities to perform auto validation of 
        different fields inside of the database via the meta class.

        Resources
        _________

        django meta docs:         https://docs.djangoproject.com/en/5.0/ref/models/options/
        django constraints docs:  https://docs.djangoproject.com/en/5.0/ref/models/constraints/
        stack overflow reference: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple

        Authors
        _______
        
        David Kennamer -_-

        """
        constraints = [
            models.UniqueConstraint(
                                    fields=["mentee","mentor"],
                                    name="unique_mentorship_request_constraint")
                ]
class MentorshipReferral(SVSUModelData,Model):
    """
    Description
    -----------
    A class to represent the referral of a mentee from one mentor to another.

    Properties
    ----------
    - mentor_from (ForeignKey): The original mentor
    - mentor_to (ForeignKey): The referred mentor
    - mentee (ForeignKey): The mentee being referred.

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    (None)

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    mentor_from = ForeignKey(
        Mentor,
        on_delete = models.CASCADE,
        related_name='created_referrals_set'
    )
    mentor_to = ForeignKey(
        Mentor,
        on_delete = models.CASCADE,
        related_name='referral_set'
    )
    mentee = ForeignKey(
        Mentee,
        on_delete = models.CASCADE
    )

class MentorReports(SVSUModelData,Model):
    """
    Description
    -----------
    MentorshipReports is a database access object.
    This class represents a report for a mentor.

    Properties
    ----------
    - mentor (ForeignKey): Represents a user who is a mentor.

    Instance Functions
    ------------------
    - create_mentor_report: Creates a report in the database using the report type, body,and mentor's ID.
    - get_report_id: Returns a specified report using an ID.
    - get_reoort_info: Returns a dictionary containing the fields of the report.

    Static Functions
    ----------------
    - NONE -

    Magic Functions
    ---------------
    - NONE -

    Authors
    -------
    Adam C.
    """
    class ReportType(TextChoices):
        """
        Description
        -----------
        An enum subclass to hold the different types of reports

        Properties
        ----------
        - BEHAVIOR

        Instance Functions
        -------------------
        (None)

        Static Functions
        -------
        (None)

        Magic Functions
        -------------
        (None)

        Authors
        -------
        Adam C.
        """
        BEHAVIOR : 'Behavior'

    mentor = ForeignKey(
        Mentor,
        on_delete = models.CASCADE
    )
    str_report_type = CharField(max_length=10, choices=ReportType.choices, default='')
    str_report_body = CharField(max_length = 3500)

    def create_mentor_report(str_provided_report_type: str, str_provided_report_body: str, int_mentor_id: int) -> bool:
        """
        Description
        -----------
        Creates a mentor report using the report type, body, and mentor's ID.

        Parameters
        ----------
        - str_provided_report_type (str): The type of report.
        - str_provided_report_body (str): The body of the report.
        - int_mentor_id (int): User ID that is the mentor.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - True (boolean): IF the mentor report was sucessfully created.
        - False (boolean): IF the mentor report was NOT created.

        Example Usage
        -------------
        >>> boolFlag = create_mentor_report('Accidentally', '', 24)
        boolFlag = False
        >>> boolFlag = create_mentor_report('Incident', 'Mentor was rude', 4)
        boolFlag = True

        Authors
        -------
        Adam C.
        """
        try:
            MentorReports.objects.create(
                str_report_type = str_provided_report_type,
                str_report_body = str_provided_report_body,
                mentor = int_mentor_id
            )
            return True
        except Exception as e:
            return False
        
    def get_report_id(int_report_id: int) -> 'MentorReports':
        """
        Description
        -----------
        - Gets a MentorReport object specified by it's ID.

        Parameters
        ----------
        -int_report_id (int): An integer specifying an object in the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - A MentorReport object.
        - Nothing if the requested MentorReport object does not exist.

        Example Usage
        -------------
        >>> cls_Report = get_report_id(2)
        cls_Report.str_report_type = 'Incident'
        cls_Report.str_report_body = 'Mentor was rude'
        cls_Report.mentor_id = 4

        Authors
        -------
        Adam C.
        """
        return MentorReports.objects.get(id = int_report_id)
    
    def get_mentor_report_info(int_report_id: int) -> dict:
        """
        Description
        -----------
        - Gets a specified MentorReport by it's ID.
        - Returns a dictionary containing the report type, body, and mentor's ID.

        Parameters
        ----------
        - int_report_id (int): Integer specifying the id of a MentorReport in
            the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - dict_Report (Dictionary, String): containing the report type, body, and mentorID.

        Example Usage
        -------------
        >>> dict_Report = get_report_id(2)
        dict_Report = {'reportType': 'Incident', 'reportBody': 'Mentor was rude', 'mentorID': 4}

        Authors
        -------
        Adam C.
        """
        cls_Report =  MentorReports.get_report_id(int_report_id)

        dict_Report = {
            "report_type" : cls_Report.str_report_type,
            "report_body" : cls_Report.str_report_body,
            "mentor_id" : cls_Report.mentor_id
        }

        return dict_Report


class Notes(SVSUModelData,Model):
    """
    Description
    -----------
    Represents an object for creating and storing notes created by a user.

    Properties
    ----------
    str_title (CharField): Title of the note for user reference.
    str_body (CharField): Main body of text the user entered.
    cls_created_on (DateField): Date the note was created on.
    user (ForeignKey): Denotes the user_id that created the note.

    Instance Functions
    ------------------
    - create_note: Creates a note using a user's id, title, body, and todays date.
    
    Static Functions
    ----------------
    - NONE

    Magic Functions
    ---------------
    - NONE

    Authors
    -------
    Justin Goupil
    """

    str_title = CharField(max_length=100)
    str_public_body = CharField(max_length=7000, null=True, blank=True)
    str_private_body = CharField(max_length=7000, null=True, blank=True)
    cls_created_on = DateField(default=date.today)


    user = ForeignKey(User, on_delete = models.CASCADE)

    @staticmethod
    def create_note(user_id: int, str_title: str, str_public_body: str, str_private_body: str):
        """
        Description
        -----------
        Creates a note using the user's id, title and body. 
        Then saves the note to the database. 

        Parameters
        ----------
        int_user_id (int): User id associated with the request.
        str_title_ (str): Title of the note.
        str_body_ (str): Body of the note.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - True (boolean): IF the note was sucessfully created.
        - False (boolean): IF the note was NOT created.
        Example Usage
        -------------

        Authors
        -------
        Justin G.
        Adam U.

        Changes
        -------
        """
        str_title = None if str_title == "" else str_title
        str_public_body = None if str_public_body == "" else str_public_body
        str_private_body = None if str_private_body == "" else str_private_body
        user = User.objects.get(id=user_id)

        if not str_title:
            return False
        elif str_public_body or str_private_body:
            Notes.objects.create(
                str_title = str_title,
                str_public_body = str_public_body,
                str_private_body = str_private_body,
                cls_created_on = date.today(),
                user = user
            )
            print("Note created")
            return True
        else:
            return False
    
    @staticmethod
    def update_note(note_id: int, new_title: str, new_pub_body: str, new_pvt_body: str) -> None:
        note = Notes.objects.get(id=note_id)

        note.str_title = new_title
        note.str_public_body = new_pub_body
        note.str_private_body = new_pvt_body
        note.save()

    @staticmethod
    def remove_note(note_id: int):
        note = Notes.objects.get(id=note_id)
        note.delete()
        
    @staticmethod
    def get_all_mentor_notes(mentor: Mentor):
        pub_notes = Notes.objects.filter(user=mentor)
        return [{
            "id" : note.id,
            "title" : note.str_title,
            "date_created" : note.cls_created_on,
            "public_note" : note.str_public_body,
            "private_note" : note.str_private_body
        } for note in pub_notes]

    @staticmethod
    def get_public_mentor_notes(mentor_id: int):
         pvt_notes = Notes.objects.filter(user=mentor_id, str_private_body__isnull=False)
         return [{
            "title" : note.str_title,
            "date_created" : note.cls_created_on,
            "public_note" : note.str_public_body
        } for note in pvt_notes]
            

        
class SystemLogs(SVSUModelData,Model):
    """
    Description
    -----------
    A class to system events

    Properties
    ----------
    - str_event (str): A description of the event that occurred 
    - cls_log_created_on (date): The date the event occured.

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    (None)

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    
    class Event(TextChoices):
        """
        Description
        -----------
        An enum subclass to hold the different user roles

        Properties
        ----------
        - LOGON_EVENT
        - CREATE_MENTORSHIP_EVENT
        - REQUEST_MENTORSHIP_EVENT
        - MENTEE_REGISTER_EVENT
        - MENTOR_REGISTER_EVENT
        - USER_DEACTIVATED

        Instance Functions
        -------------------
        (None)

        Static Functions
        -------
        (None)

        Magic Functions
        -------------
        (None)

        Authors
        -------
        
        """
        LOGON_EVENT = "User logged on"
        APPROVE_MENTORSHIP_EVENT = "Create mentorship"
        REQUEST_MENTORSHIP_EVENT = "Request mentorship"
        MENTORSHIP_TERMINATED_EVENT = "Mentorship terminated"
        MENTEE_REGISTER_EVENT = "Mentee signed up"
        MENTOR_REGISTER_EVENT = "Mentor applied"
        MENTEE_DEACTIVATED_EVENT = "Mentee deactivated"
        MENTOR_DEACTIVATED_EVENT = "Mentor deactivated"
        

    str_event = CharField(max_length=500, choices=Event.choices, default='')
    cls_log_created_on = DateField(default=date.today)
    specified_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)

    


class ProfileImg(SVSUModelData,Model):
    """
    Description
    -----------
    ProfileImg is a class that represents database access objects
    for each user's profile image.

    
    Properties
    ----------
    - user (User):      Represents the given user who has said profile
                        image.

    - img_title:        Represents the file name/location of the image
                        associated with the user.

    - img_profile:      The ImageField for the user's profile.
                        There will be a default image used as a placeholder
                        when an instance of the class is first created.

    - file_size:        Represents the size of an image

    
    Instance Functions
    ------------------
    -   get_file_size:  Returns the size of the image; set a new value to the 
                        file_size attribute if it does not currently have one.
    
    Static Functions
    ----------------
    -   create_from_user_id:    Creates a new instance of the ProfileImg class,
                                with the id of the user and the name of the image
                                passed in through parameters
    
    Magic Functions
    ---------------
    NONE

    Authors
    -------
    🌟 Isaiah Galaviz 🌟

    """
    #   The user that the image is associated with; set it as the primary key
    user = OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True,
        related_name="profile_img_query"
    )

    #   The image, its name, and its file size.
    img_title = CharField(max_length=100)
    img = ImageField(
                    upload_to="images/",
                    default=
                        "images/default_profile_picture.png"
                    )
    file_size = PositiveIntegerField(null=True, editable=False)

    #   Static function that creates a new instance of the class
    @staticmethod
    def create_from_user_id(int_user_id: int,
                            str_filename: str='images/default_profile_picture.png')->'ProfileImg':

        try:
            user_model = User.objects.get(id=int_user_id)
            new_image = ProfileImg.objects.create(user=user_model, 
                                                img_title=str_filename)
            new_image.save()
            return new_image
        except Exception as e:
            print(e)
            #Operation failed.
            return False
        
    #   Instance function that returns the size of the image
    def get_file_size(self):
        if self.file_size is None:
            try:
                self.file_size = self.img_profile.size
            except Exception as e:
                print(e)
                #Operation failed.
                return False

            self.save(update_fields=['file_size'])
        return self.file_size



class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, unique=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_reset_token(user_id):
        try:
            # Get the user instance
            user_instance = User.objects.get(pk=user_id)

          # Check if the user already has a token, delete it if it exists
            try:
                existing_token = PasswordResetToken.objects.get(user=user_id)
                existing_token.delete()
            except ObjectDoesNotExist:
                # No existing token for the user, proceed with creating a new one
                print("Existing link deleted")
                pass



            

            duplicate = True
            token = ""
            while duplicate:
                # Define the pool of characters to choose from (only uppercase letters and digits)
                characters = string.ascii_uppercase + string.digits

                # Generate a random string of length 6
                token = ''.join(random.choice(characters) for _ in range(30))

                #checks to see if token exist already
                duplicate = PasswordResetToken.objects.filter(token=token).exists()
            
            reset_token_instance = PasswordResetToken(user=user_instance, token=token)
            # Save the new instance of PasswordResetToken model
            reset_token_instance.save()

            return True, "Reset link created successfully", token
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, f"An error occurred creating your link", token
        

    
    def is_valid_token(self) -> Tuple[bool, str]: #this deletes a token if its not valid
        try:
            expiration_time = 10 ## time for a token to expire in minutes

            # Get the current time
            current_time = timezone.now()
        
            # Calculate the timestamp ten minutes ago
            ten_minutes_ago = current_time - timedelta(minutes=expiration_time)
        
            # Check if the token timestamp is greater than or equal to ten minutes ago
            if self.timestamp >= ten_minutes_ago:
                # Token is valid
                return True , "found"
            else:
                # Token expired
                self.delete() #delete expired tokens
                return False, "expired"
        except Exception as e:
            # Log or handle the exception
            return False, "ex"
    
    #deletes all expired tokens by validating them
    @staticmethod
    def delete_all_expired_reset_tokens():
        tokens = PasswordResetToken.objects.all()

        for token_record in tokens:
            if not token_record.is_valid_token(token_record):
                print(f"Expired token deleted: {token_record}")
            else:
                print(f"Token is still valid: {token_record}")

    @staticmethod
    def validate_and_reset_password(token: str, new_password: str) -> Tuple[bool, str]:
        try:
            # Retrieve the token instance based on user ID and token

          
            token_instance = PasswordResetToken.objects.get(token=token)
            
            
            valid, message = token_instance.is_valid_token()
            # Check if the token is valid
            if not valid:
                if message == "expired":
                    return False,  "Link expired, attempt reset again!"
                if message == "ex":
                    return False, "An error occoured verifying your link."
            # Delete the token since it was correct and is no longer needed
            

            user = User.objects.get(id=token_instance.user.id)
            generated_user_salt = security.generate_salt()
            user.str_password_hash = security.hash_password(new_password, generated_user_salt)
            user.str_password_salt = generated_user_salt
            user.save()
            token_instance.delete()

            
            return True, "Password successfully reset, Rerouting you to home page."  # Password reset successful
        except PasswordResetToken.DoesNotExist:
            return False,  "Invalid Link"



   