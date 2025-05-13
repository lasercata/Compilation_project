#!/usr/bin/python

## @package analex
#  Lexical Analyser package. 
#

import sys, argparse, re

DEBUG = False

LEXICAL_UNIT_CHARACTER  = "char"
LEXICAL_UNIT_KEYWORD    = "keyword"
LEXICAL_UNIT_SYMBOL     = "symbol"
LEXICAL_UNIT_IDENTIFIER = "ident"
LEXICAL_UNIT_INTEGER    = "integer"
LEXICAL_UNIT_FEL        = "fel"

keywords = [
    "and", "begin", "else", "end",
    "error", "false", "function", "get",
    "if", "in", "is", "loop", "not", "or", "out",
    "procedure", "put", "return", "then", "true", "while",
    "integer", "boolean"
]


class AnaLexException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

########################################################################                     
#### LexicalUnit classes                        ####                     
########################################################################

## Class LexicalUnit
class LexicalUnit(object):
    '''
    Mother class defining a general lexical unit

    Root class for the hierarchy of Lexical Units
    '''

    line_index = -1
    col_index = -1
    length = 0
    value = None

    def __init__(self, l: int, c: int, ln: int, value: None | str):
        '''
        Constructor of the LexicalUnit class.

        - l     : the line index of the unit ;
        - c     : the column index of the beginning of the unit ;
        - ln    : the length of the unit ;
        - value : TODO
        '''

        self.line_index = l
        self.col_index = c
        self.length = ln
        self.value = value

    def get_line_index(self) -> int:
        return self.line_index

    def get_col_index(self) -> int:
        return self.col_index

    def get_length(self) -> int:
        return self.length

    def get_value(self) -> None | str:
        return self.value

    def is_keyword(self, keyword) -> bool:
        return False

    def is_character(self, c: str) -> bool:
        return False

    def is_symbol(self, s: str) -> bool:
        return False

    def is_integer(self) -> bool:
        return False

    def is_identifier(self) -> bool:
        return False

    def is_fel(self) -> bool:
        return False

    @staticmethod
    def extract_from_line(line: str):
        '''
        Static method used to retreive a specific LexicalUnit from 
        a line of text formatted by __str__

        @param line : the line of text to process

        @return A lexical unit (instance of a child class)
        '''

        fields = line.split('\t')

        if fields[0] == Identifier.__class__.__name__:
            return Identifier(fields[1], fields[2], fields[3], fields[4])

        elif fields[0] == Keyword.__class__.__name__:
            return Keyword(fields[1], fields[2], fields[3], fields[4])

        elif fields[0] == Character.__class__.__name__:
            return Character(int(fields[1]), fields[2], fields[3], fields[4])

        elif fields[0] == Symbol.__class__.__name__:
            return Symbol(int(fields[1]), fields[2], fields[3], fields[4])

        elif fields[0] == Fel.__class__.__name__:
            return Fel(fields[1], fields[2], fields[3], fields[4])

        elif fields[0] == Integer.__class__.__name__:
            return Integer(fields[1], fields[2], fields[3], fields[4])

    def __str__(self):
        '''Returns the object as a formatted string'''

        unitValue = {'classname': self.__class__.__name__, 'lIdx': self.line_index, 'cIdx': self.col_index, 'length': self.length, 'value': self.value}
        return '%(classname)s\t%(lIdx)d\t%(cIdx)d\t%(length)d\t%(value)s\n' % unitValue

# Class to represent Identifiers
class Identifier(LexicalUnit):
    '''
    Class to represent Identifiers

    This class inherits from LexicalUnit.
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        super(Identifier, self).__init__(l, c, ln, v)

    def is_identifier(self):
        '''Return true since it is an Identifier'''

        return True

# Class to represent Keywords
class Keyword(LexicalUnit):
    '''
    Class to represent Keywords

    This class inherits from LexicalUnit.        
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        super(Keyword, self).__init__(l, c, ln, v)

    def is_keyword(self, keyword: str) -> bool:
        '''Return true since it is a keyword'''

        return self.get_value() == keyword

# Class to represent Characters
class Character(LexicalUnit):
    '''
    Class to represent Characters

    This class inherits from LexicalUnit.            
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        super(Character, self).__init__(l, c, ln, v)

    def is_character(self, c: str) -> bool:
        '''Return true since it is a character'''

        return self.get_value() == c

# Class to represent Symbols
class Symbol(LexicalUnit):
    '''
    Class to represent Symbols

    This class inherits from LexicalUnit.        
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        super(Symbol, self).__init__(l, c, ln, v)

    def is_symbol(self, s: str):
        '''Return true since it is a symbol'''

        return self.get_value() == s

# Class to represent Integers
class Integer(LexicalUnit):
    '''
    Class to represent Integers.

    This class inherits from LexicalUnit.        
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        super(Integer, self).__init__(l, c, ln, v)

    def is_integer(self):
        '''Return true since it is an integer'''

        return True

# Class to represent Fel (End of entry)
class Fel(LexicalUnit):
    '''
    Class to represent Fel (End of entry)
    This class inherits from LexicalUnit.
    '''

    def __init__(self, l: int, c: int, ln: int, v: str):
        '''Constructor'''

        super(Fel, self).__init__(l, c, ln, v)

    def is_fel(self) -> bool:
        '''Return true since it is a Fel instance'''

        return True

## Lexical analyser class
class LexicalAnalyser(object):    
    '''TODO: description'''

    ## Attribute to store the different lexical units (defined in init)
    # lexical_units: list[LexicalUnit] = []

    ## Index used to keep track of the lexical unit under treatment
    lexical_unit_index = -1

    def __init__(self):
        '''Constructor'''

        self.lexical_units: list[LexicalUnit] = []

    def analyse_line(self, lineIndex: int, line: str):
        '''
        Analyse a line and extract the lexical units. 
        The extracted lexical units are then added to the attribute `self.lexical_units`.

        @param lineIndex : index of the line in the original text
        @param line      : the line of text to analyse
        '''

        space = re.compile(r"\s")
        digit = re.compile("[0-9]")
        char = re.compile("[a-zA-Z]")
        beginColIndex = 0
        c = ''
        colIndex = 0;

        while colIndex < len(line):
            c = line[colIndex]
            unitValue = None

            if c == '/': # begin of comment or /= ...
                beginColIndex = colIndex
                colIndex = colIndex + 1
                c = line[colIndex]

                if c == '/': # it is a comment => skip rest of line
                    return

                elif c == '=':
                    # record /=
                    unitValue = Symbol(lineIndex, colIndex-1, 2, "/=")
                    colIndex = colIndex + 1

                else:
                    # record as character
                    unitValue = Character(lineIndex, colIndex-1, 1, "/")

            elif digit.match(c):
                # It is a number 
                beginColIndex = colIndex
                n = 0

                while colIndex < len(line) and (digit.match(c)):
                    n = 10*n + int(c)
                    colIndex = colIndex + 1

                    if colIndex < len(line):
                        c = line[colIndex]

                unitValue = Integer(lineIndex, beginColIndex, colIndex-beginColIndex, n)

            elif space.match(c):
                colIndex = colIndex + 1

            elif char.match(c):
                # It is either an identifier or a keyword
                beginColIndex = colIndex
                ident = ''

                while colIndex < len(line) and (char.match(c) or digit.match(c)):
                    ident = ident + c
                    colIndex = colIndex + 1

                    if colIndex < len(line): c = line[colIndex]

                if string_is_keyword(ident):
                    unitValue = Keyword(lineIndex, beginColIndex, len(ident), ident)

                else:
                    unitValue = Identifier(lineIndex, beginColIndex, len(ident), ident)

            elif c == ':': # affectation
                beginColIndex = colIndex
                colIndex = colIndex + 1
                c = line[colIndex]

                if c == '=':
                    # record :=
                    unitValue = Symbol(lineIndex, colIndex-1, 2, ":=")
                    colIndex = colIndex + 1

                else:
                    # record as character
                    unitValue = Character(lineIndex, colIndex-1, 1, ":")

            elif c == '<': # comparison
                beginColIndex = colIndex
                colIndex = colIndex + 1
                c = line[colIndex]

                if c == '=':
                    # record as symbol                
                    unitValue = Symbol(lineIndex, colIndex - 1, 2, "<=")
                    colIndex = colIndex + 1

                else:
                    # record as symbol
                    unitValue = Symbol(lineIndex, colIndex - 1, 1,"<")

            elif c == '>': # comparison
                beginColIndex = colIndex
                colIndex = colIndex + 1
                c = line[colIndex]

                if c == '=':
                    # record as symbol
                    unitValue = Symbol(lineIndex, colIndex - 1, 2, ">=")
                    colIndex = colIndex + 1

                else:
                    # record as symbol
                    unitValue = Symbol(lineIndex, colIndex - 1, 1, ">")

            elif c == '=':
                colIndex = colIndex + 1            
                c = line[colIndex]
                unitValue = Symbol(lineIndex, colIndex - 1, 1, "=")

            elif c == '.':
                colIndex = colIndex + 1
                newUnit = True
                unitValue = Fel(lineIndex, colIndex - 1, 1, ".")

            else: 
                colIndex = colIndex + 1
                unitValue = Character(lineIndex, colIndex - 1, 1, c)

            if unitValue != None:
                self.lexical_units.append(unitValue)

    def save_to_file(self, filename: str):
        '''
        Saves the lexical units to a text file.

        - filename : Name of the output file (if `""` then output to stdout)
        '''

        output_file = None
        if filename != "":
            try:
                output_file = open(filename, 'w')

            except:
                print("Error: can't open output file!")
                return

        else:
            output_file = sys.stdout

        for lexicalUnit in self.lexical_units:
            output_file.write("%s" % lexicalUnit)

        if filename != "":
            output_file.close()

    def load_from_file(self, filename: str):
        '''
        Loads lexical units from a text file.

        - filename : Name of the file to load (if `""` then stdin is used).
        '''

        input_file = None
        if filename != "":
            try:
                input_file = open(filename, 'w')
            except:
                print("Error: can't open output file!")
                return

        else:
            input_file = sys.stdin

        lines = input_file.readlines()

        if filename != "":
            input_file.close()

        for line in lines:
            lexical_unit = LexicalUnit.extract_from_line(line)
            self.lexical_units.append(lexical_unit)

    def verify_index(self) -> bool:
        '''
        Verifies that the current lexical unit index is not out of bounds.

        return True if lexical_unit_index < len(lexical_units)
        '''

        return self.lexical_unit_index < len(self.lexical_units)

    def acceptKeyword(self, keyword: str):
        '''
        Accepts a given keyword if it corresponds to the current lexical unit.

        @param keyword : string containing the keyword
        @exception AnaLexException When the keyword is not found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while keyword "+keyword+" expected!")

        if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
            self.lexical_unit_index += 1

        else:
            raise AnaLexException("Expecting keyword "+keyword+" <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

    def acceptIdentifier(self) -> str:
        '''
        Accepts an identifier if it corresponds to the current lexical unit.

        @return identifier string value
        @exception AnaLexException When no identifier is found
        '''
        if not self.verify_index():
            raise AnaLexException("Found end of entry while identifer expected!")

        if self.lexical_units[self.lexical_unit_index].is_identifier():
            value = self.lexical_units[self.lexical_unit_index].get_value()
            self.lexical_unit_index += 1

            return value

        else:
            raise AnaLexException("Expecting identifier <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

    def acceptInteger(self) -> int:
        '''
        Accepts an integer if it corresponds to the current lexical unit.

        @return integer value
        @exception AnaLexException When no integer is found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while integer value expected!")

        if self.lexical_units[self.lexical_unit_index].is_integer():
            value = self.lexical_units[self.lexical_unit_index].get_value()
            self.lexical_unit_index += 1
            return value

        else:
            raise AnaLexException("Expecting integer <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")


    def acceptFel(self):
        '''
        Accepts a Fel instance if it corresponds to the current lexical unit.

        @exception AnaLexException When no Fel is found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting .!")

        if self.lexical_units[self.lexical_unit_index].is_fel():
            self.lexical_unit_index += 1

        else:
            raise AnaLexException("Expecting end of program <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

    def acceptCharacter(self, c: str):
        '''
        Accepts a given character if it corresponds to the current lexical unit.

        @param c : string containing the character
        @exception AnaLexException When the character is not found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting character " + c + "!")

        if self.lexical_units[self.lexical_unit_index].is_character(c):
            self.lexical_unit_index += 1

        else:
            raise AnaLexException("Expecting character " + c + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")    

    def acceptSymbol(self, s: str):
        '''
        Accepts a given symbol if it corresponds to the current lexical unit.

        @param s - string containing the symbol
        @exception AnaLexException When the symbol is not found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting symbol " + s + "!")

        if self.lexical_units[self.lexical_unit_index].is_symbol(s):
            self.lexical_unit_index += 1

        else:
            raise AnaLexException("Expecting symbol " + s + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")    

    def isKeyword(self, keyword) -> bool:
        '''
        Tests if a given keyword corresponds to the current lexical unit.

        @return True if the keyword is found
        @exception AnaLexException When the end of entry is found
        '''

        if not self.verify_index():
            raise AnaLexException("Unexpected end of entry!")

        if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
            return True

        return False

    def isIdentifier(self) -> bool:
        '''
        Tests the current lexical unit corresponds to an identifier.

        @return True if an identifier is found
        @exception AnaLexException When the end of entry is found
        '''

        if not self.verify_index():
            raise AnaLexException("Unexpected end of entry!")

        if self.lexical_units[self.lexical_unit_index].is_identifier():
            return True

        return False

    def isCharacter(self, c: str) -> bool:
        '''
        Tests if a given character corresponds to the current lexical unit.

        @return True if the character is found
        @exception AnaLexException When the end of entry is found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting character " + c + "!")

        if self.lexical_units[self.lexical_unit_index].is_character(c):
            return True

        return False

    def isInteger(self) -> bool:
        '''
        Tests the current lexical unit corresponds to an integer.

        @return True if an integer is found
        @exception AnaLexException When the end of entry is found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting integer value!")

        if self.lexical_units[self.lexical_unit_index].is_integer():
            return True

        return False

    def isSymbol(self, s: str) -> bool:
        '''
        Tests if a given symbol corresponds to the current lexical unit.

        @return True if the symbol is found
        @exception AnaLexException When the end of entry is found
        '''

        if not self.verify_index():
            raise AnaLexException("Found end of entry while expecting symbol " + s + "!")

        if self.lexical_units[self.lexical_unit_index].is_symbol(s):
            return True

        return False

    def get_value(self) -> str:
        '''
        Returns the value of the current lexical unit

        @return value of the current unit
        '''

        return self.lexical_units[self.lexical_unit_index].get_value()

    def init_analyser(self):
        '''Initializes the lexical analyser'''

        self.lexical_unit_index = 0

########################################################################                          

def string_is_keyword(s: str) -> bool:
    '''
    Tests if a keyword is in the table of keywords.

    @return True if the keyword is found
    '''

    return s in keywords


########################################################################
def main_analex(file_content: str, fn_out: str):
    '''
    Launches the lexical analysis of the program `file_content`.

    - file_content     : the content of the file (the NNP program) ;
    - fn_out           : the name of the potential output file. If "", prints to stdout instead ;
    '''

    lexical_analyser = LexicalAnalyser()

    lineIndex = 0
    for line in file_content.split('\n'):
        line = line.rstrip('\r\n')
        lexical_analyser.analyse_line(lineIndex, line)
        lineIndex = lineIndex + 1

    lexical_analyser.save_to_file(fn_out)

########################################################################

