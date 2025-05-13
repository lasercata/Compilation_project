from typing import Dict


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
        self.scope = scope
        self.address = address
        self.value = value
    
    #Getters and setters for the attributes of the class
    def __getName__(self, name):
        return self.name
    
    def __getType__(self, type):
        return self.type

    def __getScope__(self, scope):
        return self.scope
    
    def __getAddress__(self, address):
        return self.address
    
    def __getValue__(self, value):
        return self.value
    
    def __setName__(self, name):
        self.name = name
    
    def __setType__(self, type):
        self.type = type
    
    def __setScope__(self, scope):
        self.scope = scope
    
    def __setAddress__(self, address):
        self.address = address
    
    def __setValue__(self, value):
        self.value = value
    
class IdentifierTable:
    
    """This class is meant to be used as a table for identifiers."""
    
    def __init__(self):
        """this method is used to initialize a table for identifiers."""
        self.__dict__: Dict[str, IdentifierCarac]={} #initializing the table as a dictionary containing the identifiers as keys and their characteristics as values.
     

    def addIdentifier(self, nom : str, carac: IdentifierCarac):
        """this method is used to add an identifier to the table."""
        if nom not in self.__dict__:
            self.__dict__[nom] = carac
        else:
            raise Exception("Identifier already exists")
        
    
    def deleteIdentifier(self, identifierName: str):
        """this method is used to delete an identifier from the table."""
        if identifierName in self.__dict__:
            del self.__dict__[identifierName]
        else:
            raise Exception("Identifier does not exist")
    
    def getIdentifier(self, name: str):
        """this method is used to get an identifier from the table."""
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise Exception("Identifier does not exist")    
    
    def getTable(self):
        """this method is used to get the table."""
        return self.__dict__
    
    def printTable(self):
        """ AI GENERATED CODE
        This method is used to print the table."""

        headers = ["name", "type", "scope", "address", "value"]

        #building the rows of the table
        rows = [
            [str(identifier.name), str(identifier.type), str(identifier.scope),
            str(identifier.address), str(identifier.value)]
            for identifier in self.__dict__.values()
        ]

        # Calculating the maximum width of each column
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))

        # function to format each row
        def format_row(row):
            return "| " + " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"

        # separation line
        separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

        # printing the table
        print(separator)
        print(format_row(headers))
        print(separator)
        for row in rows:
            print(format_row(row))
        print(separator)

    
    
    

