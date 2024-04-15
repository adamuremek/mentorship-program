from django.db.models import *
from .svsu_model import SVSUModelData
from django.core.exceptions import ObjectDoesNotExist

class Interest(SVSUModelData,Model):
    """
    Description
    -----------
    A class outlining the model for user interests

    Properties
    ----------
    - strInterest - descriptive text regaurding what this interest is
    - isDefaultInterest - is true only if we added the initial interest at the start of the app, false for user defined interests

    Instance Functions
    -------------------
    (None)

    Static Functions
    -------
    - get_default_interests: Returns a list of the default interests
    - get_initial_default_interest_strings: Returns a string list of hard-coded
        default interest strings

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    strInterest = CharField(max_length=100, null=False,unique=True)
    isDefaultInterest = BooleanField(default=False)


    @staticmethod
    def create_interest(str_interest : str, bool_default : bool = False) -> 'Interest' :
        """
        Description
        -----------
        Creates an interest given a name and boolean value to determine 
        if the interest is a default interest.


        Example Usage
        _____________
        >>> my_interest = create_interest("Computer Science")


        Authors
        -------
        Justin Goupil
        """
        #Create the interest and save it to the database in one line.
        try:
            return Interest.objects.create(
                strInterest = str_interest,
                isDefaultInterest = bool_default
            )
        except :
            return None
        
    
    @staticmethod
    def get_interest(str_interest_name : str ) -> 'Interest' :
        """
        Description
        -----------
        Gets an interest by name.


        Example Usage
        _____________
        >>> my_interest = get_interest("Computer Science")


        Authors
        -------
        Justin Goupil
        """
        
        try:
            #Find the first instance of the interest in the database and return the object.
            return Interest.objects.filter(str_interest = str_interest_name).first()
        except:
            return None
    
    @staticmethod
    def update_interest(str_interest_name : str, bool_default : bool, str_new_interest_name : str = None) -> 'Interest' :
        """
        Description
        -----------
        Updates an interest with a new default value or interest name.


        Example Usage
        _____________
        >>> my_interest = update_interest("Netwoking", True, "Networking")


        Authors
        -------
        Justin Goupil
        """
        try:
            #Find the first instance of the interest in the database and return the object.
            interest : 'Interest' = Interest.objects.filter(str_interest = str_interest_name)
            
            if str_new_interest_name != None :
                interest.strInterest = str_new_interest_name
            
            interest.isDefaultInterest = bool_default

            #save the instance to the database
            interest.save()

            return interest
        except:
            return None
        
    @staticmethod
    def create_default_interests():
        
        default_interests = [
            'Artificial Intelligence', 
            'Computer Graphics', 
            'Data Structures & Algorithms',
            'Networking',
            'Operating Systems',
            'Embedded Systems',
            'Cloud Computing',
            'Software Engineering',
            'Distrubuted Systems',
            'Game Development',
            'Cybersecurity',
            'System Analysis']
        
        for interest in default_interests:
            Interest.get_or_create_interest(interest)
    
    @staticmethod
    def delete_interest(str_interest_name : str) -> 'Interest' :
        """
        Description
        -----------
        Removes an interest from the database.


        Example Usage
        _____________
        >>> my_interest = delete_interest("Compter Science")


        Authors
        -------
        Justin Goupil
        """
        try:
            #Find the first instance of the interest in the database and return the object.
            interest : 'Interest' = Interest.objects.filter(str_interest = str_interest_name)
            interest.delete()

            return interest
        except:
            return None

    @staticmethod
    def get_or_create_interest(str_interest : str) -> 'Interest':
        """
        Description
        -----------
        attempts to get a given interest, if it does not exist in the db create it


        Example Usage
        _____________
        my_interest = Interest.get_or_create_interest("Buffalo Breeding")


        Authors
        -------
        David Kennamer )-(
        """
        try:
            ret_int = Interest.objects.get(strInterest = str_interest)
            return ret_int
        except ObjectDoesNotExist:
            Interest.objects.create(strInterest=str_interest).save()


    #convinence methods
    @staticmethod
    def get_default_interests() -> QuerySet:
        """
        Description
        -----------
        Returns a list of all default interest objects

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        (None)

        Returns
        -------
        - QuerySet: The set of all default interest objects

        Example Usage
        -------------

        >>> Interest.get_default_interests()
        '<[Interest: c++, Interest: python, Interest: html, ...]>'

        Authors
        -------
        
        """
        return Interest.objects.filter(isDefaultInterest=True)

    # def __str__(self) -> str:
    #     return self.strInterest