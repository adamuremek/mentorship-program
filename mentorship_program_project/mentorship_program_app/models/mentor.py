#django imports
from django.db import models
from django.db.models import *
from django.core.exceptions import ValidationError
from .svsu_model import SVSUModelData
from .user import User
from .organization import Organization
from utils import security


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

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cache = security.Decorators.FunctionCache()
        self.has_maxed_mentees = self.cache.create_cached_function(self.has_maxed_mentees)

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
        if org.admin_mentor.id==self.id:
            return True
        return False


    def get_shared_organizations(self,other : 'Mentor'):
        """
        returns a list of organizations shared between two mentors,
        the list will be empty if no mentors exists
        """
        return self.organizations.all() & other.organizations.all()
        
    int_max_mentees = IntegerField(default=4)


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