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

    """
        returns a list of string properties
        that we do not want front end technologies
        to see
    """
    @staticmethod
    def get_backend_only_properties()->list[str]:
        return ["save","delete"]
    
    """
        sets all properties that are read only in the black list to None

        returns a reference to ourselfs for convinient usage
    """
    def sanatize_black_properties(self,black_list : list[str] = []):
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

    #PLACEHOLDER: Change to User_Accounts
    #   User_Accounts have a User_Profile
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

    #PLACEHOLDER: Move to User_Profiles
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
            return security.Decorators.require_check(lambda req :
                                                         security.is_logged_in(req.session)
                                                         and
                                                         User.from_session(req.session).is_mentor(),
                                                     
                                                     alternate_view
                                                     )
        @staticmethod
        def require_loggedin_mentee(alternate_view):
            return security.Decorators.require_check(lambda req :
                                                         security.is_logged_in(req.session)
                                                         and
                                                         User.from_session(req.session).is_mentee(),

                                                        alternate_view
                                                     )



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
    
    @staticmethod
    def create_request(intMentorID: int, intMenteeID: int):
        """
        2/25/2024
        Creates a relationship given a mentorID and menteeID.
        """
        obj = MentorshipRequest.objects.create(
            mentor_id = intMentorID,
            mentee_id = intMenteeID
        )
        return obj

    def getRequest(intId: int):
        """
        2/25/2024
        returns a MentorshipRequest object. 
        """
        return MentorshipRequest.objects.get(id = intId)


    def getRequestInfo(intId: int):
        """
        2/25/2024
        returns a dictionary containing the User id of the mentorID and menteeID for a MentorshipRequest object
        """

        clsRequest =  MentorshipRequest.getRequest(intId)

        dictRequest = {
            "mentorID" : clsRequest.mentor_id,
            "menteeID" : clsRequest.mentee_id
        }

        return dictRequest
    
    def remove_request(intMentorID: int, intMenteeID: int):
        """
        2/25/2024 Removes a request from the database. 
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
    class ReportType(TextChoices):
        BEHAVIOR : 'Behavior'

    mentor = ForeignKey(
        Mentor,
        on_delete = models.CASCADE
    )
    strReportType = CharField(max_length=10, choices=ReportType.choices, default='')
    strReportBody = CharField(max_length = 3500)

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
