from typing import Dict


class IdentifierType:
    """This class is used to define the different types of identifiers."""

    INTEGER = "integer"
    BOOLEAN = "boolean"
    FUNCTION = "function"
    PROCEDURE = "procedure"

class IdentifierCarac:
    def __init__(self, type_: IdentifierType | str, name: str, scope: str, isIn: bool | None = None, isOut: bool | None = None, address=None, value=None):
        """
        type: type of the identifier, defined higher in the code;
        name: name of the identifier;
        scope: scope of the identifier, can be either "global", "local" or "parameter";
        address: address of the identifier in memory if definable, default value None;
        value: value of the identifier, default value None.
        """

        self.type = type_
        self.name = name
        self.scope = scope
        self.isIn = isIn
        self.isOut = isOut
        self.address = address
        self.value = value
    
    #Getters and setters for the attributes of the class
    def __getName__(self, name):
        return self.name
    
    def __getType__(self, type):
        return self.type

    def __getScope__(self, scope):
        return self.scope
    
    def __getIn__(self, isIn):
        return self.isIn
    
    def __getOut__(self, isOut):
        return self.isOut
    
    def __getAddress__(self, address):
        return self.address
    
    def __getValue__(self, value):
        return self.value
    
    def __setName__(self, name):
        self.name = name
    
    def __setType__(self, type_):
        self.type = type_
    
    def __setScope__(self, scope):
        self.scope = scope
    
    def __setIn__(self, isIn):
        self.isIn = isIn
    
    def __setOut__(self, isOut):
        self.isOut = isOut
    
    def __setAddress__(self, address):
        self.address = address
    
    def __setValue__(self, value):
        self.value = value
    
class IdentifierTable:
    """This class is meant to be used as a table for identifiers."""
    
    def __init__(self):
        """this method is used to initialize a table for identifiers."""

        self.tbl: Dict[str, IdentifierCarac] = {} #initializing the table as a dictionary containing the identifiers as keys and their characteristics as values.
        self.addr_global = 0  # address for global variables
        self.addr_param = 0   # address for parameters
        self.addr_local = 0   # address for local variables
        self.addr_proc_func = 0
        
        
    def addIdentifier(self, nom: str, carac: IdentifierCarac):
        """Add an identifier to the table, with automatic address assignment"""

        if nom in self.tbl:
            raise Exception(f"Identifier '{nom}' already exists")

        if carac.scope == "global":
            if carac.type in [IdentifierType.PROCEDURE, IdentifierType.FUNCTION]:
                carac.address = self.addr_proc_func
                self.addr_proc_func += 1
            else:
                carac.address = self.addr_global
                self.addr_global += 1

        elif carac.scope == "parameter":
            carac.address = self.addr_param
            self.addr_param += 1

        elif carac.scope == "local":
            carac.address = self.addr_local
            self.addr_local += 1

        self.tbl[nom] = carac  
        

    
    def assign_procedure_address(self, nom: str):
        """this method is used to assign an address to a procedure after its declaration."""
        if nom not in self.tbl:
            raise Exception(f"Identifier '{nom}' not found in the table.")
        
        max_addr = max(
            (c.address for c in self.tbl.values()
            if c.scope == "global" and c.type not in [IdentifierType.FUNCTION, IdentifierType.PROCEDURE] and isinstance(c.address, int)),
            default=-1
        )
        self.tbl[nom].address = max_addr + 1




    
    def deleteIdentifier(self, identifierName: str):
        """this method is used to delete an identifier from the table."""

        if identifierName in self.tbl:
            del self.tbl[identifierName]

        else:
            raise Exception("Identifier does not exist")
    
    def getIdentifier(self, name: str):
        """this method is used to get an identifier from the table."""

        if name in self.tbl:
            return self.tbl[name]

        else:
            raise Exception("Identifier does not exist")    
    
    def getTable(self):
        """this method returns only the identifier entries (filters out internal variables)."""
        
        return {k: v for k, v in self.tbl.items() if isinstance(v, IdentifierCarac)}
    
    def printTable(self):
        
        """AI GENERATED METHOD Prints the table of identifiers."""

        headers = ["name", "type", "scope", "In", "Out", "address", "value"]

        # Construction de la liste des lignes à partir des objets IdentifierCarac
        rows = [
            [
                str(identifier.name),
                str(identifier.type),
                str(identifier.scope),
                str(identifier.isIn),
                str(identifier.isOut),
                str(identifier.address),
                str(identifier.value)
            ]
            for identifier in self.tbl.values()
            if type(identifier) != int
        ]

        # Calcul de la largeur maximale de chaque colonne
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))

        # Fonction pour formater une ligne
        def format_row(row):
            return "| " + " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"

        # Ligne de séparation
        separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

        # Affichage du tableau
        print(separator)
        print(format_row(headers))
        print(separator)
        for row in rows:
            print(format_row(row))
        print(separator)


