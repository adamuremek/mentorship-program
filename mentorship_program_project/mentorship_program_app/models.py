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

        >>> get_backend_only_properties()
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

        >>> getUserLogin('fake@email.com')
        'adlkfy8o90q23gb876df'

        Authors
        -------
        
        """
        security.black_list(self,self.get_backend_only_properties() + black_list)
        return self




class Interest(SVSUModelData,Model):
    """

    """
    strInterest = CharField(max_length=100, null=False,unique=True)
    isDefaultInterest = BooleanField(default=False)



    #convinence methods

    """
        convinence function to return an array of default interest objects 
        idk the return type of djangos queries so its not typed atm
    """
    @staticmethod
    def get_default_interests():
        return Interest.objects.filter(isDefaultInterest=True)

    #simply returns an array representing the inital default interests that we want
    #to be populated to the database
    @staticmethod 
    def get_initial_default_interest_strings()-> list[str]:
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
        generate a list of backend only properties appended to the 
        general blackouted properties

        see SVSUModelData as to what this is overloading
    """
    def get_backend_only_properties(self)-> list[str]:
        return super().get_backend_only_properties() + [
                "strPasswordHash",
                "strPasswordSalt",
                "check_valid_password"
                ]

    class Role(TextChoices):
        ADMIN = 'Admin'
        MENTOR = 'Mentor'
        MENTEE = 'Mentee'
        MENTOR_PENDING = 'MentorPending'
        GRADUATED = 'Graduated'
        DECLINED = 'Declined'

    clsEmailAddress =  EmailField(null=True,unique=True)  
    strPasswordHash =  CharField(max_length=1000, null=True, blank=False)
    strPasswordSalt =  CharField(max_length=1000, null=True, blank=False)
    strRole = CharField(max_length=15, choices=Role.choices, default='')
    clsDateJoined = DateField(default=date.today)
    clsActiveChangedDate = DateField(default=date.today)
    blnActive = BooleanField(default=True)
    blnAccountDisabled =  BooleanField(default=False)

    strFirstName: CharField =  CharField(max_length=747,null=True)
    strLastName =  CharField(max_length=747, null=True) 
    strPhoneNumber =  CharField(max_length=15, null=True)
    clsDateofBirth = DateField(default=date.today)
    strGender = CharField(max_length=35, default='')
    strPreferredPronouns = CharField(max_length=50, null=True)

    #image field with url location
    imgUserProfile = ImageField(
                                upload_to="images/",
                                default=
                                    "images/default_profile_picture.png"
                                )

    #foregn key fields
    interests = models.ManyToManyField(Interest)

    """
    returns true if we have a mentor account in the database
    """
    def is_mentor(self)->bool:
        try:
            self.mentor
            return True
        except ObjectDoesNotExist:
            return False

    """
    returns true if we have a mentee acount in the database
    """
    def is_mentee(self)->bool:
        try:
            self.mentee
            return True
        except ObjectDoesNotExist:
            return False
    """
    returns true if the incoming pasword matches the stored password for the 
    current user
    """
    def check_valid_password(self,password_plain_text : str)->bool:
        return security.hash_password(password_plain_text,self.strPasswordHash) ==\
                self.strPasswordHash

    """
    returns a NON SAVED user object that has the password properly hashed
    and salt correctly generated it's your responsibility to save this object 
    if you want it to persist in the db YOU HAVE BEEN WARNED >_>
    """
    @staticmethod
    def create_from_plain_text_and_email(password_plain_text : str,
                                         email : str)->'User':
        generated_user_salt = security.generate_salt()
        #TODO: emails need to be validated, send a sacrifical lamb
        #to the regex gods
        return User.objects.create(
                    strPasswordHash = security.hash_password(
                                            password_plain_text,
                                            generated_user_salt),
                    strPasswordSalt = generated_user_salt,
                    clsEmailAddress = email
                )

    """
    returns a new user object from given session data if the user is logged in
    note that the user must be logged in for this to work, if they are not logged in 
    returns None
    """
    @staticmethod 
    def from_session(session)->'User':
        if not security.is_logged_in(session): return None

        return User.objects.get(id=session.get("user_id"))

    """
    returns true if the given email password combination is
    a valid account, otherwise false
    """
    @staticmethod
    def check_valid_login(email_str : str,password_plain_text : str):
        try:
            u = User.objects.get(clsEmailAddress=email_str)
        except ObjectDoesNotExist:
            return False
        return u.check_valid_password(password_plain_text)

    def getUserInfo(self):
        user_info = {
            "EmailAddress": self.clsEmailAddress,
            "Role": self.strRole,
            "DateJoined": self.clsDateJoined,
            "ActiveChangedDate": self.clsActiveChangedDate,
            "Active": self.blnActive,
            "AccountDisabled": self.blnAccountDisabled,
            "FirstName": self.strFirstName,
            "LastName": self.strLastName,
            "PhoneNumber": self.strPhoneNumber,
            "DateOfBirth": self.clsDateofBirth,
            "Gender": self.strGender,
            "PreferredPronouns": self.strPreferredPronouns
        }

        if hasattr(self, 'biographies') and self.biographies:
            user_info["Biography"] = self.biographies.strBio

        return user_info
    
    
    """
    namespace for decorators that apply to views SPECIFICALLY to limit the kind of user 
    that can interact with the view. 

    We would prefer these in the security file, but since that will cause a circular dependency,
    and these have to do entierly with users it makes sense to place them here
    """
    class Decorators:
        @staticmethod
        def require_loggedin_mentor(alternate_view):
            validator = lambda req : security.is_logged_in(req.session) \
                                     and User.from_session(req.session).is_mentor()
            return security.Decorators.require_check(validator, alternate_view)
        
        @staticmethod
        def require_loggedin_mentee(alternate_view):
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
        user_model.strRole = User.Role.MENTOR
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
        user_model.strRole = User.Role.MENTEE
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
    
    class Meta:
        """
        django provides the capabilities to perform auto validation of 
        different fields inside of the database via the meta class.

        Resources
        _________

        django meta docs:         https://docs.djangoproject.com/en/5.0/ref/models/options/
        django constraints docs:  https://docs.djangoproject.com/en/5.0/ref/models/constraints/
        stack overflow reference: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple

        """
        constraints = [
            models.UniqueConstraint(
                                    fields=["mentee","mentor"],
                                    name="unique-mentorship-request-constraint")
                ]


    def create_request(intMentorID: int, intMenteeID: int):
        """
        Description
        -----------
        Creates a mentorship request using two user ids.

        Parameters
        ----------
        - intMentorID (int): User ID that is the mentor.
        - intMenteeID (int): User ID that is the mentee.

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
                mentor_id = intMentorID,
                mentee_id = intMenteeID
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
    
    def remove_request(intMentorID: int, intMenteeID: int):
        """
        Description
        -----------
        Removes a mentorship request from the database.

        Parameters
        ----------
        - intMentorID: (int):
        - intMenteeID: (int):

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
            MentorshipRequest.objects.filter(mentor = intMentorID, mentee = intMenteeID).delete()
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

    def create_mentor_report(strProvidedReportType: str, strProvidedReportBody: str, intMentorID: int):
        """
        Description
        -----------
        Creates a mentor report using the report type, body, and mentor's ID.

        Parameters
        ----------
        - strProvidedReportType (str): The type of report.
        - strProvidedReportBody (str): The body of the report.
        - intMentorID (int): User ID that is the mentor.

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
                mentor = intMentorID
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
        -intId (int): An intiger specifying an object in the database.

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

