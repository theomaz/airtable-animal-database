from airtable import Airtable

class Session(object):
    def __init__(self, base_key, table_name, API_key=None):
        self.base_key = base_key 
        self.table_name = table_name 
        self.API_key = API_key 

    def Authenticate(self, base_key, table_name, API_key=None):
        """
        Authenticate airtable API with entry table.

        Returns: Airtable class object
        """

        return Airtable(base_key, table_name, API_key)