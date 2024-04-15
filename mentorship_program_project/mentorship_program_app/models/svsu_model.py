from utils import security
"""
class containing functions we want in every one of our 
models, but not necessarily model classes
"""
class SVSUModelData():
    """
    Description
    -----------
    A class containing functions we want in every one
    of our models, but not necessarily model classes.

    Properties
    ----------
    (None)

    Instance Functions
    -------------------
    - sanitize_black_properties: Sets all read-only properties
        in the blacklist to None

    Static Functions
    -------
    - get_backend_only_properties:
        Returns a string list of properties only for back-end technologies

    Magic Functions
    -------------
    (None)

    Authors
    -------
    
    """
    #ensure that this model is not stored in the database
    #it is ONLY a logical model
    abstract = True

    @staticmethod
    def get_backend_only_properties():
        
        """
        Description
        -----------
        Get a static list of properties to be hidden from front-end technologies

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

        >>> SVSUModelData.get_backend_only_properties()
        '["save", "delete"]'

        Authors
        -------
        
        """
        return ["save","delete"]
    

    def sanitize_black_properties(self, black_list : list[str] = []) -> 'SVSUModelData':
        """
        Description
        -----------
        Sets all read-only properties in the blacklist to None

        Parameters
        ----------
        (None)

        Optional Parameters
        -------------------
        - black_list ([str]): The list of properties on the blacklist.

        Returns
        -------
        - SVSUModelData: Returns itself for convenience.

        Example Usage
        -------------

        >>> svsu_data_model.sanititze_black_properties()
        'svsu_data_model'

        Authors
        -------
        
        """
        security.black_list(self,self.get_backend_only_properties() + black_list)
        return self