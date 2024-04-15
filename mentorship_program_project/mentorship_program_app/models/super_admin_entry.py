#django imports
from django.db import models
from django.db.models import *

#project imports
from .svsu_model import SVSUModelData
from .user import User




class SuperAdminEntry(SVSUModelData,Model):
    """
    this class represents a list of super admin mentors in the database

    if you have an entry in this table you are super admin,
    if you do not have an entry, you are not super admin
    """
    bool_enabled = BooleanField(default=True) #can be used to turn off admin
    user_account = OneToOneField(User, on_delete=models.CASCADE,related_name="admin_entry")