from django.forms import CharField
from .svsu_model import SVSUModelData
from django.db.models import *

class WhitelistedEmails(SVSUModelData,Model):
    # 320 is max length of an email address
    str_email = CharField(max_length = 320)