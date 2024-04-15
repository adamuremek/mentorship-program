#django imports
from django.db import models
from django.db.models import *
from .svsu_model import SVSUModelData
from .user import User



class ProfileImg(SVSUModelData,Model):
    """
    Description
    -----------
    ProfileImg is a class that represents database access objects
    for each user's profile image.

    
    Properties
    ----------
    - user (User):      Represents the given user who has said profile
                        image.

    - img_title:        Represents the file name/location of the image
                        associated with the user.

    - img_profile:      The ImageField for the user's profile.
                        There will be a default image used as a placeholder
                        when an instance of the class is first created.

    - file_size:        Represents the size of an image

    
    Instance Functions
    ------------------
    -   get_file_size:  Returns the size of the image; set a new value to the 
                        file_size attribute if it does not currently have one.
    
    Static Functions
    ----------------
    -   create_from_user_id:    Creates a new instance of the ProfileImg class,
                                with the id of the user and the name of the image
                                passed in through parameters
    
    Magic Functions
    ---------------
    NONE

    Authors
    -------
    🌟 Isaiah Galaviz 🌟
    """
    #   The user that the image is associated with; set it as the primary key
    user = OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True,
        related_name="profile_img_query"
    )

    #   The image, its name, and its file size.
    img_title = CharField(max_length=100)
    img = ImageField(
                    upload_to="images/",
                    default=
                        "images/default_profile_picture.png"
                    )
    file_size = PositiveIntegerField(null=True, editable=False)

    #   Static function that creates a new instance of the class
    @staticmethod
    def create_from_user_id(int_user_id: int,
                            str_filename: str='images/default_profile_picture.png')->'ProfileImg':

        try:
            user_model = User.objects.get(id=int_user_id)
            new_image = ProfileImg.objects.create(user=user_model, 
                                                img_title=str_filename)
            new_image.save()
            return new_image
        except Exception as e:
            print(e)
            #Operation failed.
            return False
        
    #   Instance function that returns the size of the image
    def get_file_size(self):
        if self.file_size is None:
            try:
                self.file_size = self.img_profile.size
            except Exception as e:
                print(e)
                #Operation failed.
                return False

            self.save(update_fields=['file_size'])
        return self.file_size