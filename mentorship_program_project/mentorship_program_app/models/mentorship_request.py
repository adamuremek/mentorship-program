#django imports
from django.db import models
from django.db.models import *
from .svsu_model import SVSUModelData
from .user import User
from .system_logs import SystemLogs
from .mentee import Mentee

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

        #prevent accepting of new requests when you are already in a mentorship
        if self.mentee.is_mentee() and self.mentee.mentee.mentor != None:
            print("they have a mentor")
            return False

        # record logs
        # record the mentee since the mentor can be gathered from it later
        mentor,mentee = session_user.create_mentorship_from_user_ids(
                                                    self.mentee.id,
                                                    self.mentor.id
                                                    )
        print(mentor, mentee)
        if mentor == None or mentee == None:
            
            return False

        # record logs
        # record the mentee since the mentor can be gathered from it later
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
        David Kennamer 
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


    class ErrorCode:
        MENTOR_MAXED_MENTEES = -1
        MENTEE_MAXED_REQUEST_AMOUNT = -2
        DATABASE_ERROR = -3
        MENTEE_HAS_MENTOR = -4
        
        @staticmethod
        def error_code_to_string(code : int)->str:
            return [
             "MENTOR_MAXED_MENTEES",
             "MENTEE_MAXED_REQUEST_AMOUNT",
             "DATABASE_ERROR",
             "MENTEE_HAS_MENTOR"
            ][-(code+1)]

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
        either the request object or an error code indicating what occured
        while making the request

        you can find these error codes under MentorshipRequest.ErrorCode

        Example Usage
        -------------
        >>> error_code = create_request(13, 16)
        error_code = MentorshipRequest.ErrorCode.MENTEE_MAXED_REQUEST_AMOUNT
        >>> request_object = create_request(5, 24)
        request_object = valid request object

        

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
                return MentorshipRequest.ErrorCode.MENTOR_MAXED_MENTEES

            #prevent mentees from creating too many requests
            requester_user_account = User.objects.get(id=requester_id)
            if requester_user_account.is_mentee():
                if requester_user_account.mentee.has_maxed_request_count():
                    return MentorshipRequest.ErrorCode.MENTEE_MAXED_REQUEST_AMOUNT
                if requester_user_account.mentee.mentor != None:
                    print("we will not finish the request!")
                    return MentorshipRequest.ErrorCode.MENTEE_HAS_MENTOR

            mentor_ship_request = MentorshipRequest.objects.create(
                mentor_id = int_mentor_user_id,
                mentee_id = int_mentee_user_id,
                requester = requester_id
            )

            # record logs
            SystemLogs.objects.create(str_event=SystemLogs.Event.REQUEST_MENTORSHIP_EVENT, 
                                    specified_user= User.objects.get(id=requester_id))

            return mentor_ship_request
        except Exception as e:
            print(e)
            return MentorshipRequest.ErrorCode.DATABASE_ERROR

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