from django.db import models
from django.db.models import *
from datetime import date


from utils import security

# Create your models here.

class Users(Model):
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
 
    #PLACEHOLDER: Session_Information
    #   Separate session into its own table or keep with User_Accounts?
    strSessionID = CharField(max_length=255,default='')
    strSessionKeyHash = CharField(max_length=100,default='')

    
    def __str__(self):
        return self.firstname + ' ' + self.lastname
    
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
                                         email : str)->'Users':
        generated_user_salt = security.generate_salt()
        #TODO: emails need to be validated, send a sacrifical lamb
        #to the regex gods
        return Users.objects.create(
                    strPasswordHash = security.hash_password(
                                            password_plain_text,
                                            generated_user_salt),
                    strPasswordSalt = generated_user_salt,
                    clsEmailAddress = email
                )




class Biographies(Model):
    """

    """
    intUserID = OneToOneField(
        "Users",
        on_delete = models.CASCADE,
        primary_key=True
    )

    strBio = CharField(max_length=5000, null=True)

    def __str__(self):
        return self.bio


class Interests(Model):
    """

    """
    strInterest = CharField(max_length=100, null=False)


    def __str__(self):
        return self.strInterest


class User_Interests(Model):
    """

    """   
    intUserID = ForeignKey(
        "Interests",
        on_delete = models.CASCADE
    )
    intInterestID = ForeignKey(
        "Users",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentors(Model):
    """

    """
    intUserID = OneToOneField(
        "Users",
        on_delete = models.CASCADE
    )
    intOrganizationID = ForeignKey(
        "Organizations",
        on_delete = models.CASCADE
    )
    intMaxMentees = IntegerField(default=4)#PLACEHOLDER: default=4
    intRecommendations = IntegerField(default=0)
    strJobTitle = CharField(max_length=100)

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentees(Model):
    """

    """
    intUserID = OneToOneField(
        "Users",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentorships(Model):
    """

    """
    intMentorID = ForeignKey(
        "Mentors",
        on_delete = models.CASCADE
    )
    intMenteeID = ForeignKey(
        "Mentees",
        on_delete = models.CASCADE
    )

    clsStartDate = DateField(default=date.today, null=False)
    clsEndDate = DateField(null=True)

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentorship_Requests(Model):
    """

    """
    intMentorID = ForeignKey(
        "Mentors",
        on_delete = models.CASCADE
    )
    intMenteeID = ForeignKey(
        "Mentees",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentorship_Referrals(Model):
    """

    """
    intReferrerUserID = ForeignKey(
        "Users",
        on_delete = models.CASCADE
    )

    intMentorID = ForeignKey(
        "Mentors",
        on_delete = models.CASCADE
    )

    intMenteeID = ForeignKey(
        "Mentees",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return "Default" #PLACEHOLDER


class Mentor_reports(Model):
    """
    
    """
    #PLACEHOLDER: ReportTypes needs more choices.
    class ReportType(TextChoices):
        BEHAVIOR : 'Behavior'

    intMentorID = ForeignKey(
        "Mentors",
        on_delete = models.CASCADE
    )
    strReportType = CharField(max_length=10, choices=ReportType.choices, default='')
    strReportBody = CharField(max_length = 3500)

class Notes(Model):
    """

    """
    intUserID = ForeignKey(
        "Users",
        on_delete = models.CASCADE
    )
    strTitle = CharField(max_length=100)
    strBody = CharField(max_length=7000)
    clsCreatedOn = DateField(default=date.today)

    def __str__(self):
        return "Default" #PLACEHOLDER


class Organizations(Model):
    """
    
    """
    strName = CharField(max_length=100)
    strIndustryType = CharField(max_length=100)

    def __str__(self):
        return "Default" #PLACEHOLDER


class Organization_Admins(Model):
    """
    
    """

    intUserID = ForeignKey(
        "Users",
        on_delete = models.CASCADE
    )
    intOrganizationID = ForeignKey(
        "Organizations",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return "Default" #PLACEHOLDER

class System_Logs(Model):
    """
    
    """

    strActivity = CharField(max_length = 500)
    clsCreatedOn = DateField(default=date.today)

    def __str__(self):
        return "Default" #PLACEHOLDER 
