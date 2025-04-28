class IdentifierType:

    """This class is used to define the different types of identifiers."""

    INTEGER = "integer"
    BOOLEAN = "boolean"
    FUNCTION = "function"
    PROCEDURE = "procedure"

class IdentifierCarac:

    def __init__(self, type: IdentifierType, name: str, scope: str, address=None, value=None):
        """type: type of the identifier, defined higher in the code;
        name: name of the identifier;
        scope: scope of the identifier, can be either "global", "local" or "parameter";
        address: address of the identifier in memory if definable, default value None;
        value: value of the identifier, default value None."""
        self.type = type
        self.name = name
        #self.scope = scope
        self.address = address
        self.value = value
    
    #Getters and setters for the attributes of the class
    def __getName__(self, name):
        return self.name
    
    def __getType__(self, type):
        return self.type

    """def __getScope__(self, scope):
        return self.scope"""
    
    def __getAddress__(self, address):
        return self.address
    
    def __getValue__(self, value):
        return self.value
    
    def __setName__(self, name):
        self.name = name
    
    def __setType__(self, type):
        self.type = type
    
    """xdef __setScope__(self, scope):
        self.scope = scope"""
    
    def __setAddress__(self, address):
        self.address = address
    
    def __setValue__(self, value):
        self.value = value
    
class IdentifierTable:
    """This class is meant to be used as a table for identifiers."""
    
    def __init__(self):
        """this method is used to initialize a table for identifiers."""
        #TO DO 

    def addIdentifier(self, identifier: IdentifierCarac):
        """this method is used to add an identifier to the table."""
        #TO DO
    
    def deleteIdentifier(self, identifier: IdentifierCarac):
        """this method is used to delete an identifier from the table."""
        #TO DO
    
    def getIdentifier(self, name: str):
        """this method is used to get an identifier from the table."""
        #TO DO
    
    def getTable(self):
        """this method is used to get the table."""
        return self.table
    
    def printTable(self):
        """this method is used to print the table."""
        for identifier in self.table:
            print(identifier.name, identifier.type, identifier.scope, identifier.address, identifier.value, "\n")
    
    
    
    

