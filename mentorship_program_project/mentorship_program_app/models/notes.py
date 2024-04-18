from django.db import models
from django.db.models import *
from .svsu_model import SVSUModelData
from .user import User
from .mentor import Mentor
from django.utils import timezone

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
    cls_created_on = DateField(default=timezone.now)


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