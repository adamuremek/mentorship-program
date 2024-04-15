#django imports
from django.conf import settings
from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
from .svsu_model import SVSUModelData
from .user import User
from utils import security



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
        #### DO NOT MOVE THIS IMPORT ###
        #### It needs to be here to prevent a circular import ###
        from .mentorship_request import MentorshipRequest

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