"""
FILE NAME: models.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED:

-------------------------------------------------------------------------------
FILE PURPOSE:
Defines all models to store object into the database.

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

from django.conf import settings
from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist

from datetime import date

from utils import security

import os

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
    - strInterest
    - isDefaultInterest

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

    #simply returns an array representing the inital default interests that we want
    #to be populated to the database
    @staticmethod 
    def get_initial_default_interest_strings()-> list[str]:
        """
        Description
        -----------
        Returns a list representing the inital default interests that we want
        to be populated to the database

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - list[str]: The set of all default interest objects

        Example Usage
        -------------

        >>> Interest.get_initial_default_interest_strings()
        '[c++, python, html, ...]'

        Authors
        -------
        
        """
        return [
                "c++",
                "python",
                "html",
                "javascript",
                "webdev",
                "godot",
                "calculus",
                "AI"
                ]
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
    - cls_date_of_birth
    - str_gender
    - str_preferred_pronouns
    - img_user_profile
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

    str_first_name: CharField =  CharField(max_length=747,null=True)
    str_last_name =  CharField(max_length=747, null=True) 
    str_phone_number =  CharField(max_length=15, null=True)
    cls_date_of_birth = DateField(default=date.today)
    str_gender = CharField(max_length=35, default='')
    str_preferred_pronouns = CharField(max_length=50, null=True)

    #image field with url location
    img_user_profile = ImageField(
                                upload_to="images/",
                                default=
                                    "images/default_profile_picture.png"
                                )

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
        - str: Mentor if mentor esle MEntee
        read the python :p ^

        Example Usage
        -------------

        >>> user_joe.get_database_role_str()
        'Mentor'

        Authors
        -------
        
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
            return True
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
            return True
        except ObjectDoesNotExist:
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
        - User: the created user object

        Example Usage
        -------------

        >>> User.create_from_plain_text_and_email("password", "joeshmo@email.com")
        NewUserObject1

        Authors
        -------
        
        """
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
            "PreferredPronouns": self.str_preferred_pronouns
        }

        if hasattr(self, 'biographies') and self.biographies:
            user_info["Biography"] = self.biographies.strBio

        return user_info
    
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

        Magic Functions
        -------------
        (None)

        Authors
        -------
        
        """
        @staticmethod
        def require_logged_in_mentor(alternate_view):
            """
            Commenter Note: I'm not entirely sure the exact details of how this
            works. I know what it does on a high level (see class comment), but
            I'm not 100% sure on the intricacies. Whoever wrote this should
            double-check that I have everything right.

            Description
            -----------

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
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_mentor()
            return security.Decorators.require_check(validator, alternate_view)
        
        @staticmethod
        def require_logged_in_mentee(alternate_view):
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_mentee()
            return security.Decorators.require_check(validator, alternate_view)

class Biographies(SVSUModelData,Model):
    """

    """
    user = OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key=True
    )

    strBio = CharField(max_length=5000, null=True)

class Organization(SVSUModelData,Model):
    """
    
    """
    strName = CharField(max_length=100)
    strIndustryType = CharField(max_length=100)

    admins = models.ManyToManyField('Mentor')

class Mentor(SVSUModelData,Model):

    intMaxMentees = IntegerField(default=4)
    intRecommendations = IntegerField(default=0)
    strJobTitle = CharField(max_length=100)



    account = OneToOneField(
        User,
        on_delete = models.CASCADE
    )


    """
    creates and saves a mentor and user account to the database that uses the given
    username and password 

    returns a reference to this object
    """
    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'Mentee':
        user_model = User.create_from_plain_text_and_email(password_plain_text,email)
        user_model.save()

        mentor = Mentor.objects.create(account=user_model)
        mentor.save()
        return mentor

class Mentee(SVSUModelData,Model):
    """
    Description
    -----------

    Properties
    ----------

    Instance Functions
    ------------------

    Static Functions
    ----------------

    Magic Functions
    ---------------

    Authors
    -------

    """
    account = OneToOneField(
        "User",
        on_delete = models.CASCADE
    )
    
    """
    creates and saves a mentee and user account to the database that uses the given
    username and password 

    returns a reference to this object
    """
    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'Mentee':
        user_model = User.create_from_plain_text_and_email(password_plain_text,email)
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
    def create_request(int_mentor_id: int, int_mentee_id: int):
        """
        Description
        -----------
        Creates a mentorship request using two user ids.

        Parameters
        ----------
        - int_mentor_id (int): User ID that is the mentor.
        - int_mentee_id (int): User ID that is the mentee.

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
        """

        try:
            MentorshipRequest.objects.create(
                mentor_id = int_mentor_id,
                mentee_id = int_mentee_id
            )
            return True
        except Exception as e:
            return False

    def get_request_id(intId: int):
        """
        Description
        -----------
        - Gets a MentorshipRequest object specified by it's ID.

        Parameters
        ----------
        -intId (int): An intiger specifying an object in the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - A MentorshipRequest object.
        - Nothing if the requested MentorshipRequest object does not exist.

        Example Usage
        -------------
        >>> clsRequest = get_request_id()
        clsRequest.mentee = 7
        clsRequest.mentor = 8

        Authors
        -------
        Justin G.
        """
        return MentorshipRequest.objects.get(id = intId)


    def get_request_info(intId: int):
        """
        Description
        -----------
        - Gets a specified MentorshipRequest by it's ID.
        - Returns a dictionary containing the user ID of the mentor and mentee.

        Parameters
        ----------
        - intId (int): Integer specifying the id of a MentorshipRequest in
            the database.
        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - dictRequest (Dictionary, String): Containing mentorID and menteeID.
        Example Usage
        -------------
        >>> dictRequest = get_request_id(5)
        dictRequest = {'mentorID': 1, 'menteeID': 2}

        Authors
        -------
        Justin G.
        """

        clsRequest =  MentorshipRequest.get_request_id(intId)

        dictRequest = {
            "mentorID" : clsRequest.mentor_id,
            "menteeID" : clsRequest.mentee_id
        }

        return dictRequest
    
    def remove_request(int_mentor_id: int, int_mentee_id: int):
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

class MentorshipReferral(SVSUModelData,Model):
    """

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
        BEHAVIOR : 'Behavior'

    mentor = ForeignKey(
        Mentor,
        on_delete = models.CASCADE
    )
    strReportType = CharField(max_length=10, choices=ReportType.choices, default='')
    strReportBody = CharField(max_length = 3500)

    def create_mentor_report(strProvidedReportType: str, strProvidedReportBody: str, int_mentor_id: int):
        """
        Description
        -----------
        Creates a mentor report using the report type, body, and mentor's ID.

        Parameters
        ----------
        - strProvidedReportType (str): The type of report.
        - strProvidedReportBody (str): The body of the report.
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
                strReportType = strProvidedReportType,
                strReportBody = strProvidedReportBody,
                mentor = int_mentor_id
            )
            return True
        except Exception as e:
            return False
        
    def get_report_id(intID: int):
        """
        Description
        -----------
        - Gets a MentorReport object specified by it's ID.

        Parameters
        ----------
        -intId (int): An integer specifying an object in the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - A MentorReport object.
        - Nothing if the requested MentorReport object does not exist.

        Example Usage
        -------------
        >>> clsReport = get_report_id(2)
        clsReport.strReportType = 'Incident'
        clsReport.strReportBody = 'Mentor was rude'
        clsReport.mentor_id = 4

        Authors
        -------
        Adam C.
        """
        return MentorReports.objects.get(id = intID)
    
    def get_mentor_report_info(intReportID: int):
        """
        Description
        -----------
        - Gets a specified MentorReport by it's ID.
        - Returns a dictionary containing the report type, body, and mentor's ID.

        Parameters
        ----------
        - intReportId (int): Integer specifying the id of a MentorReport in
            the database.

        Optional Parameters
        -------------------
        - NONE -

        Returns
        -------
        - dictReport (Dictionary, String): containing the report type, body, and mentorID.

        Example Usage
        -------------
        >>> dictReport = get_report_id(2)
        dictReport = {'reportType': 'Incident', 'reportBody': 'Mentor was rude', 'mentorID': 4}

        Authors
        -------
        Adam C.
        """
        clsReport =  MentorReports.get_report_id(intReportID)

        dictReport = {
            "reportType" : clsReport.strReportType,
            "reportBody" : clsReport.strReportBody,
            "mentorID" : clsReport.mentor_id
        }

        return dictReport


class Notes(SVSUModelData,Model):
    strTitle = CharField(max_length=100)
    strBody = CharField(max_length=7000)
    clsCreatedOn = DateField(default=date.today)


    user = ForeignKey(
        User,
        on_delete = models.CASCADE
    )

class SystemLogs(SVSUModelData,Model):
    """
    
    """
    
    strActivity = CharField(max_length = 500)
    clsCreatedOn = DateField(default=date.today)

