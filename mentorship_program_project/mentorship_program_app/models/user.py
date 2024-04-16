#django imports
from django.conf import settings
from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

#standard python imports
from typing import Callable
from typing import List, Dict
from django.db.models import Q

from .interest import Interest
from .svsu_model import SVSUModelData
#project imports
from utils import security
from django.utils import timezone

from utils import security


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
        self.function_cache = security.Decorators.FunctionCache()
        
        #decorate cachable functions on the init level so python understands when to remove
        #the cached data
        self.is_mentee = self.function_cache.create_cached_function(self.is_mentee)
        self.is_mentor = self.function_cache.create_cached_function(self.is_mentor)



    @property 
    def str_full_name(self):
        first_name = self.str_first_name if self.str_first_name != None else " "
        last_name =  self.str_last_name if self.str_last_name != None else " "
        return first_name + " " + last_name
    
    def is_an_org_admin(self)->bool:
        from .organization import Organization
        try:
            Organization.objects.get(admin_mentor_id=self.mentor.id)
            return True
        except:
            return False

    def get_recomended_users(self,limit : int =4):
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




        sub_query = ""
        not_taken = "1=1"
        if self.is_mentee():
            #### DO NOT MOVE THIS IMPORT ###
            #### It needs to be here to prevent a circular import ###
            from .mentee import Mentee
            sub_query = f"SELECT COUNT(*) FROM mentorship_program_app_mentorshiprequest WHERE mentee_id={self.id} AND mentor_id=t1.user_id"
           
            if self.mentee.mentor:
                not_taken = f"""
                                SELECT id <> {self.mentee.mentor.id} as value FROM 
                                        mentorship_program_app_mentor as m 
                                    WHERE
                                        m.account_id = tu.id
                            """
        else:
            sub_query = \
                f"SELECT COUNT(*) FROM mentorship_program_app_mentorshiprequest WHERE mentee_id=t1.user_id AND mentor_id={self.id}"

            not_taken = f"SELECT COUNT(mentor_id)<1 FROM mentorship_program_app_mentee WHERE account_id = tu.id"
        

        query = \
                    f"""
                    SELECT DISTINCT t1.user_id AS id,
                                    str_first_name,
                                    str_last_name,
                                    COUNT(*) as likeness,
                                    ({sub_query}) as is_requested_by_session
                       FROM 
                            mentorship_program_app_user_interests AS t1,
                            mentorship_program_app_user_interests AS t2,
                            mentorship_program_app_user AS tu
                       WHERE t2.user_id={self.id} 
                            AND t1.interest_id = t2.interest_id 
                            AND t1.user_id = tu.id
                            AND tu.str_role = '{self.get_opposite_database_role_string()}'
                            AND ({not_taken})
                            AND NOT tu.bln_account_disabled
                       GROUP BY t1.user_id,tu.str_first_name,tu.str_last_name,tu.id
                       ORDER BY likeness DESC
                       LIMIT {limit};
                    """
        return User.objects.raw(query)

        
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

    def get_organization(self) -> list[str]:
        """
        Description
        -----------
        Gets the names of the organizations that a user belongs to

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - [str]: A list of organizations associated with the user

        Example Usage
        -------------

        >>> User.get_organization()
        '[ABC Corp]'

        Authors
        -------
        Adam C.
        """
        
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentor import Mentor
        
        if self.is_mentor:
            #prefetch_related to reduce database queries
            this_mentor = Mentor.objects.prefetch_related('organization').get(account=self)
            organizations = this_mentor.organization.all()
            #ideally this check isn't necessary since all mentors must have an organization, but some of the test users
            #don't currently have orgs, so this handles those cases
            if organizations.exists():  
                return [org.str_org_name for org in organizations]
            else:
                return ['No organization associated']
        return ['None']
    
    def get_job_title(self) -> str:
        """
        Description
        -----------
        Gets a user's job title if they are a mentor

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - str: A user's job title if they are a mentor

        Example Usage
        -------------

        >>> User.get_job_title()
        'Software Developer'

        Authors
        -------
        Adam C.
        """

        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentor import Mentor
        
        if self.is_mentor:
            this_mentor = Mentor.objects.get(account=self)
            if(this_mentor.str_job_title != ""):
                return this_mentor.str_job_title
            else:
                return 'No job title associated'
    def get_experience(self) -> str:
        """
        Description
        -----------
        Gets a user's job title if they are a mentor

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - str: A user's job title if they are a mentor

        Example Usage
        -------------

        >>> User.get_job_title()
        'Software Developer'

        Authors
        -------
        Adam C.
        """
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentor import Mentor

        if self.is_mentor:
            this_mentor = Mentor.objects.get(account=self)
            if(this_mentor.str_experience != ""):
                return this_mentor.str_experience
            else:
                return ''

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
       # from .interest import Interest
       # from .organization import Organization
        
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
    cls_date_joined = DateField(default=timezone.now)
    cls_active_changed_date = DateField(default=timezone.now)
    bln_active = BooleanField(default=True)
    bln_account_disabled =  BooleanField(default=False)

    str_first_name : CharField =  CharField(max_length=747,null=True)
    str_last_name : CharField =  CharField(max_length=747, null=True) 
    str_phone_number : CharField = CharField(max_length=20, null=True)
    str_last_login_date = DateField(default=timezone.now)
    str_gender = CharField(max_length=35, default='')
    str_preferred_pronouns = CharField(max_length=50, null=True)
    str_bio = CharField(max_length=5000, default='')
    bln_notifications = BooleanField(default=True)
    #foregn key fields
    interests = models.ManyToManyField(Interest)
        
    def has_requested_user(self,other_user_id : int):
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentorship_request import MentorshipRequest
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


    def has_requested_user_all(self, user_ids: List[int]) -> Dict[int, bool]:
        """
        Retrieve MentorshipRequest objects involving the current user and any of the specified user IDs.

        Parameters:
        - user_ids (List[int]): List of user IDs to check for MentorshipRequests.

        Returns:
        - Dict[int, bool]: A dictionary indicating whether a MentorshipRequest exists between each user and the current user.
        """
    
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentorship_request import MentorshipRequest

        # Initialize a query that combines all individual conditions using logical OR (|)
        combined_query = Q()
        for user_id in user_ids:
            combined_query |= Q(mentor=self, mentee_id=user_id) | Q(mentee=self, mentor_id=user_id)

        # Fetch all mentorship requests matching any of the combined conditions in one query
        mentorship_requests = MentorshipRequest.objects.filter(combined_query)

        # Initialize dictionary to track requested users
        requested_users = {}

        # Loop through each user ID
        for user_id in user_ids:
            # Check if any mentorship request exists for the user
            user_query = Q(mentor=self, mentee_id=user_id) | Q(mentee=self, mentor_id=user_id)
            user_requests = mentorship_requests.filter(user_query)
            user_exists = user_requests.exists()
            
            

            if user_exists:
                requested_users[user_id] = True  # Mark the user as involved
            else:
                requested_users[user_id] = False  # Mark the user as not involved

        return requested_users





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

    def get_shared_organizations(self,other : 'User'):
        """
        returns a set of organizations that the two given users share
        """
        #only mentors have organizations
        if not (self.is_mentor() and other.is_mentor()): return None

        return self.mentor.organizations & other.mentor.organizations




    def get_first_shared_organization(self,other : 'User'):
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
        
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentorship_request import MentorshipRequest
        
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
            "Gender": self.str_gender,
            "PreferredPronouns": self.str_preferred_pronouns,
            "str_bio" : self.str_bio
        }



        return user_info
    
    @staticmethod
    def make_user_inactive(user :"User", reason : str):
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentee import Mentee
        from .mentor import Mentor
        from .mentorship_request import MentorshipRequest
        from .system_logs import SystemLogs

        user.bln_active = False
        # if you're a mentee, get rid of your mentor and all pending requests
        if user.is_mentee():
            mentee_account = Mentee.objects.get(account_id=user.id)
            mentee_account.mentor = None
            mentee_account.save()
            MentorshipRequest.objects.filter(mentee_id=user.id).delete()
            SystemLogs.objects.create(str_event=SystemLogs.Event.MENTEE_INACTIVATED_EVENT, specified_user= User.objects.get(id=user.id), str_details=reason)
        # if you're a mentor, get rid of your mentees and get rid of your pending requests
        if user.is_mentor():
            mentor_account = Mentor.objects.get(account_id=user.id)
            MentorshipRequest.objects.filter(mentor_id=user.id).delete()
            mentees_for_mentor = Mentee.objects.filter(mentor_id=mentor_account.id)
            for mentee in mentees_for_mentor:
                mentee.mentor = None
            Mentee.objects.bulk_update(mentees_for_mentor, ['mentor'])
            SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_INACTIVATED_EVENT, specified_user= User.objects.get(id=user.id), str_details=reason)
        user.save()
        
    @staticmethod
    def reactivate_user(user: "User"):
        if user.bln_account_disabled:
            return "Account cannot be reactivated, user is banned"
        user.bln_active = True
        user.save()
        
    @staticmethod
    def disable_user(user:"User", reason):
        user.bln_account_disabled = True
        user.save()
        
        User.make_user_inactive(user, reason)
    
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
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .profile_image import ProfileImg

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
