#django imports
from django.conf import settings
from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
from .svsu_model import SVSUModelData



class Organization(SVSUModelData,Model):
    """
    Description
    -----------
    A class to store information about an organization.

    Properties
    ----------
    - str_org_name (str): The name of the organization
    - str_industry_type (str): The industry the organization operate in

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
    str_org_name = CharField(max_length=100)
    str_industry_type = CharField(max_length=100)

    admin_mentor = OneToOneField('Mentor', related_name='administered_organizations', on_delete=models.CASCADE, null=True) 

    @staticmethod
    def create_org(str_org : str, str_orgType : str = None) -> 'Organization' :
        try:
            return Organization.objects.create(
                str_org_name = str_org,
                str_industry_type = str_orgType
            )
        except :
            return None
    
    @staticmethod
    def get_org(str_name : str) -> 'Organization' :
        try:
            return Organization.objects.filter(str_org_name = str_name).first()
        except:
            return None

    @staticmethod
    def update_orgName(str_name : str, str_new_org_name : str = None) -> 'Organization' :
        try:
            company : 'Organization' = Organization.objects.filter(str_org_name = str_name)
        
            if str_new_org_name != None :
                company.str_org_name = str_new_org_name

            company.save()

            return company
        except:
            return None
        
    @staticmethod
    def update_orgType(str_name : str, str_new_company_type : str = None) -> 'Organization' :
        try:
            company : 'Organization' = Organization.objects.filter(str_org_name = str_name)
        
            if str_new_company_type != None :
                company.str_industry_type = str_new_company_type

            company.save()

            return company
        except:
            return None
        
    @staticmethod
    def create_default_company_names():
        default_company_names = [
            "Auto Owner's Insurance",
            "Dow",
            "Google"]
        
        for company in default_company_names:
            Organization.get_or_create_company_name(company)
    
    @staticmethod
    def delete_company(str_name : str) -> 'Organization' :
        try:
            company : 'Organization' = Organization.objects.filter(str_org_name = str_name)
            company.delete()

            return company
        except:
            return None
        
    @staticmethod
    def get_or_create_company_name(str_name : str) -> 'Organization':
        try:
            ret_company = Organization.objects.get(str_org_name = str_name)
            return ret_company
        except ObjectDoesNotExist:
            #TODO: put in try catch to account for connection issues
            Organization.objects.create(str_org_name=str_name).save()
