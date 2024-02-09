from django.db import models
from django.db.models import *
from datetime import date

from utils import security

# Create your models here.


class Interest(Model):
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
    def get_initial_default_interest_strings()->[str]:
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


class User(Model):
    """

    """
    #PLACEHOLDER: Change to User_Accounts
    #   User_Accounts have a User_Profile
    class Role(TextChoices):
        ADMIN = 'Admin'
        MENTOR = 'Mentor'
        MENTEE = 'Mentee'

    clsEmailAddress =  EmailField(null=True,unique=True)  
    strPasswordHash =  CharField(max_length=100, null=True, blank=False)
    strPasswordSalt =  CharField(max_length=100, null=True, blank=False)
    strRole = CharField(max_length=10, choices=Role.choices, default='')
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
 

    #foregn key fields
    interests = models.ManyToManyField(Interest)

    #returns true if the incoming plain text hashes out to our stored
    #password hash
    def check_valid_password(self,password_plain_text : str)->bool:
        return security.hash_password(password,self.strPasswordSalt) ==\
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



class Biographies(Model):
    """

    """
    user = OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key=True
    )

    strBio = CharField(max_length=5000, null=True)



class Organization(Model):
    """
    
    """
    strName = CharField(max_length=100)
    strIndustryType = CharField(max_length=100)

    admins = models.ManyToManyField('Mentor')


class Mentor(Model):
    intMaxMentees = IntegerField(default=4)
    intRecommendations = IntegerField(default=0)
    strJobTitle = CharField(max_length=100)



    account = OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    orginization = ForeignKey(
        Organization,
        on_delete = models.CASCADE
    )



class Mentee(Model):
    """

    """
    account = OneToOneField(
        "User",
        on_delete = models.CASCADE
    )


class MentorshipRequest(Model):
    """

    """
    mentor = ForeignKey(
        Mentor,
        on_delete = models.CASCADE
    )
    mentee = ForeignKey(
        Mentee,
        on_delete = models.CASCADE
    )


class MentorshipReferral(Model):
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


class MentorReports(Model):
    class ReportType(TextChoices):
        BEHAVIOR : 'Behavior'

    mentor = ForeignKey(
        Mentor,
        on_delete = models.CASCADE
    )
    strReportType = CharField(max_length=10, choices=ReportType.choices, default='')
    strReportBody = CharField(max_length = 3500)

class Notes(Model):
    strTitle = CharField(max_length=100)
    strBody = CharField(max_length=7000)
    clsCreatedOn = DateField(default=date.today)


    user = ForeignKey(
        User,
        on_delete = models.CASCADE
    )



class SystemLogs(Model):
    """
    
    """
    
    strActivity = CharField(max_length = 500)
    clsCreatedOn = DateField(default=date.today)
