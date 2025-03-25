#!/usr/bin/python

## 	@package analex
# 	Lexical Analyser package. 
#

import sys, argparse, re

DEBUG = False

LEXICAL_UNIT_CHARACTER			= "char"
LEXICAL_UNIT_KEYWORD			= "keyword"
LEXICAL_UNIT_SYMBOL				= "symbol"
LEXICAL_UNIT_IDENTIFIER			= "ident"
LEXICAL_UNIT_INTEGER			= "integer"
LEXICAL_UNIT_FEL				= "fel"

keywords = [ \
	"and", "begin", "else", "end", \
	"error", "false", "function", "get", \
	"if", "in", "is", "loop", "not", "or", "out", \
	"procedure", "put", "return", "then", "true", "while", \
	"integer", "boolean" \
	]


class AnaLexException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
########################################################################				 	
#### LexicalUnit classes					    ####				 	
########################################################################

## Class LexicalUnit
#
# Root class for the hierarchy of Lexical Units
class LexicalUnit(object):
	line_index = -1
	col_index = -1	
	length = 0
	value = None
	
	## The constructor
	def __init__(self, l, c, ln, value):
		self.line_index = l
		self.col_index = c
		self.length = ln
		self.value = value
		
	def get_line_index(self):
		return self.line_index
	
	def get_col_index(self):
		return self.col_index
		
	def get_length(self):
		return self.length
		
	def get_value(self):
		return self.value
	
	def is_keyword(self, keyword):
		return False

	def is_character(self, c):
		return False

	def is_symbol(self, s):
		return False
	
	def is_integer(self):
		return False
	
	def is_identifier(self):
		return False
		
	def is_fel(self):
		return False
	
        ## Static method used to retreive a specific LexicalUnit from 
        # a line of text formatted by __str__
        # @param line the line of text to process
        # @return A lexical unit (instance of a child class)
	@staticmethod
	def extract_from_line(line):
		fields = line.split('\t')
		if fields[0] == Identifier.__class__.__name__:
			return Identifier(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Keyword.__class__.__name__:
			return Keyword(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Character.__class__.__name__:
			return Character(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Symbol.__class__.__name__:
			return Symbol(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Fel.__class__.__name__:
			return Fel(fields[1], fields[2], fields[3], fields[4])
		elif fields[0] == Integer.__class__.__name__:
			return Integer(fields[1], fields[2], fields[3], fields[4])
	
        ## Returns the object as a formatted string
	def __str__(self):
		unitValue = {'classname':self.__class__.__name__,'lIdx':self.line_index,'cIdx':self.col_index,'length':self.length,'value':self.value}
		return '%(classname)s\t%(lIdx)d\t%(cIdx)d\t%(length)d\t%(value)s\n' % unitValue

## Class to represent Identifiers
#
# This class inherits from LexicalUnit.
class Identifier(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Identifier, self).__init__(l, c, ln, v)

	## Return true since it is an Identifier
	def is_identifier(self):
		return True

## Class to represent Keywords
#
# This class inherits from LexicalUnit.		
class Keyword(LexicalUnit):
	## The constructor
	def __init__(self, l, c, ln, v):
		super(Keyword, self).__init__(l, c, ln, v)
		
        ## Return true since it is a keyword
	def is_keyword(self, keyword):
		return self.get_value() == keyword

## Class to represent Characters
#
# This class inherits from LexicalUnit.			
class Character(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Character, self).__init__(l, c, ln, v)

        ## Return true since it is a character
	def is_character(self, c):
		return self.get_value() == c

## Class to represent Symbols
#
# This class inherits from LexicalUnit.		
class Symbol(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Symbol, self).__init__(l, c, ln, v)

        ## Return true since it is a symbol
	def is_symbol(self, s):
		return self.get_value() == s

## Class to represent Integers
#
# This class inherits from LexicalUnit.		
class Integer(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Integer, self).__init__(l, c, ln, v)
	
        ## Return true since it is an integer
	def is_integer(self):
		return True

## Class to represent Fel (End of entry)
#
# This class inherits from LexicalUnit.			
class Fel(LexicalUnit):
        ## The constructor
	def __init__(self, l, c, ln, v):
		super(Fel, self).__init__(l, c, ln, v)

        ## Return true since it is a Fel instance
	def is_fel(self):
		return True
		
## Lexical analyser class
#
class LexicalAnalyser(object):	
        ## Attribute to store the different lexical units
	lexical_units = []

        ## Index used to keep track of the lexical unit under treatment
	lexical_unit_index = -1
	
        ## The constructor
	def __init__(self):
		lexical_units = []
	
        ## Analyse a line and extract the lexical units. 
        # The extracted lexical units are then added to the attribute lexical_units.
        # @param lineIndex index of the line in the original text
        # @param line the lien of text to analyse
	def analyse_line(self, lineIndex, line):
		space = re.compile("\s")
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
				while colIndex<len(line) and (digit.match(c)):
					n = 10*n + int(c)
					colIndex = colIndex + 1
					if colIndex < len(line): c = line[colIndex]
				unitValue = Integer(lineIndex, beginColIndex, colIndex-beginColIndex, n)
			elif space.match(c):
				colIndex = colIndex + 1
			elif char.match(c):
				# It is either an identifier or a keyword
				beginColIndex = colIndex
				ident = ''
				while colIndex<len(line) and (char.match(c) or digit.match(c)):
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
					unitValue = Symbol(lineIndex, colIndex-1, 2, "<=")
					colIndex = colIndex + 1
				else:
					# record as symbol
					unitValue = Symbol(lineIndex, colIndex-1, 1,"<")
			elif c == '>': # comparison
				beginColIndex = colIndex
				colIndex = colIndex + 1
				c = line[colIndex]
				if c == '=':
					# record as symbol
					unitValue = Symbol(lineIndex, colIndex-1, 2, ">=")
					colIndex = colIndex + 1
				else:
					# record as symbol
					unitValue = Symbol(lineIndex, colIndex-1, 1, ">")
			elif c == '=':
				colIndex = colIndex + 1			
				c = line[colIndex]
				unitValue = Symbol(lineIndex, colIndex-1, 1, "=")
			elif c == '.':
				colIndex = colIndex + 1
				newUnit = True
				unitValue = Fel(lineIndex, colIndex-1, 1, ".")
			else: 
				colIndex = colIndex + 1
				unitValue = Character(lineIndex, colIndex-1, 1, c)
			if unitValue != None:
				self.lexical_units.append(unitValue)
		
        ## Saves the lexical units to a text file.
        # @param filename Name of the output file (if "" then output to stdout)
	def save_to_file(self, filename):
		output_file = None
		if filename != "":
			try:
				output_file = open(filename, 'w')
			except:
				print("Error: can\'t open output file!")
				return
		else:
			output_file = sys.stdout
		
		for lexicalUnit in self.lexical_units:
			output_file.write("%s" % lexicalUnit)
			
		if filename != "":
			output_file.close()
	
        ## Loads lexical units from a text file.
        # @param filename Name of the file to load (if "" then stdin is used)
	def load_from_file(self, filename):
		input_file = None
		if filename != "":
			try:
				input_file = open(filename, 'w')
			except:
				print("Error: can\'t open output file!")
				return
		else:
			input_file = sys.stdint
		
		lines = input_file.read_lines()
			
		if filename != "":
			input_file.close()
		
		for line in lines:
			lexical_unit = LexicalUnit.extract_from_line(line)
			self.lexical_units.append(lexical_unit)

        ## Verifies that the current lexical unit index is not out of bounds
        # return True if lexical_unit_index < len(lexical_units)
	def verify_index(self):
		return self.lexical_unit_index < len(self.lexical_units)
		
        ## Accepts a given keyword if it corresponds to the current lexical unit.
        # @param keyword string containing the keyword
        # @exception AnaLexException When the keyword is not found
	def acceptKeyword(self, keyword):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while keyword "+keyword+" expected!")
		if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting keyword "+keyword+" <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

        ## Accepts an identifier if it corresponds to the current lexical unit.
        # @return identifier string value
        # @exception AnaLexException When no identifier is found
	def acceptIdentifier(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while identifer expected!")
		if self.lexical_units[self.lexical_unit_index].is_identifier():
			value =  self.lexical_units[self.lexical_unit_index].get_value()
			self.lexical_unit_index += 1
			return value
		else:
			raise AnaLexException("Expecting identifier <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")
	
        ## Accepts an integer if it corresponds to the current lexical unit.
        # @return integer value
        # @exception AnaLexException When no integer is found
	def acceptInteger(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while integer value expected!")
		if self.lexical_units[self.lexical_unit_index].is_integer():
			value = self.lexical_units[self.lexical_unit_index].get_value()
			self.lexical_unit_index += 1
			return value
		else:
			raise AnaLexException("Expecting integer <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")
	

        ## Accepts a Fel instance if it corresponds to the current lexical unit.
        # @exception AnaLexException When no Fel is found
	def acceptFel(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting .!")
		if self.lexical_units[self.lexical_unit_index].is_fel():
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting end of program <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")

        ## Accepts a given character if it corresponds to the current lexical unit.
        # @param c string containing the character
        # @exception AnaLexException When the character is not found
	def acceptCharacter(self, c):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting character " + c + "!")
		if self.lexical_units[self.lexical_unit_index].is_character(c):
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting character " + c + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")	

        ## Accepts a given symbol if it corresponds to the current lexical unit.
        # @param s string containing the symbol
        # @exception AnaLexException When the symbol is not found
	def acceptSymbol(self, s):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting symbol " + s + "!")
		if self.lexical_units[self.lexical_unit_index].is_symbol(s):
			self.lexical_unit_index += 1
		else:
			raise AnaLexException("Expecting symbol " + s + " <line "+str(self.lexical_units[self.lexical_unit_index].get_line_index())+", column "+str(self.lexical_units[self.lexical_unit_index].get_col_index())+"> !")	
	
        ## Tests if a given keyword corresponds to the current lexical unit.
        # @return True if the keyword is found
        # @exception AnaLexException When the end of entry is found
	def isKeyword(self, keyword):
		if not self.verify_index():
			raise AnaLexException("Unexpected end of entry!")
		if self.lexical_units[self.lexical_unit_index].is_keyword(keyword):
			return True
		return False

        ## Tests the current lexical unit corresponds to an identifier.
        # @return True if an identifier is found
        # @exception AnaLexException When the end of entry is found
	def isIdentifier(self):
		if not self.verify_index():
			raise AnaLexException("Unexpected end of entry!")
		if self.lexical_units[self.lexical_unit_index].is_identifier():
			return True
		return False

	## Tests if a given character corresponds to the current lexical unit.
        # @return True if the character is found
        # @exception AnaLexException When the end of entry is found
	def isCharacter(self, c):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting character " + c + "!")
		if self.lexical_units[self.lexical_unit_index].is_character(c):
			return True
		return False			

        ## Tests the current lexical unit corresponds to an integer.
        # @return True if an integer is found
        # @exception AnaLexException When the end of entry is found
	def isInteger(self):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting integer value!")
		if self.lexical_units[self.lexical_unit_index].is_integer():
			return True
		return False			

        ## Tests if a given symbol corresponds to the current lexical unit.
        # @return True if the symbol is found
        # @exception AnaLexException When the end of entry is found
	def isSymbol(self, s):
		if not self.verify_index():
			raise AnaLexException("Found end of entry while expecting symbol " + s + "!")
		if self.lexical_units[self.lexical_unit_index].is_symbol(s):
			return True
		return False			

        ## Returns the value of the current lexical unit
        # @return value of the current unit
	def get_value(self):
		return self.lexical_units[self.lexical_unit_index].get_value()
			
        ## Initializes the lexical analyser
	def init_analyser(self):
		self.lexical_unit_index = 0
	
########################################################################				 		 

## Tests if a keyword is in the table of keywords
# @return True if the keyword is found
def string_is_keyword(s):
	return keywords.count(s) != 0

		 
########################################################################				 	
def main():
	parser = argparse.ArgumentParser(description='Do the lexical analysis of a NNP program.')
	parser.add_argument('inputfile', type=str, nargs=1, help='name of the input source file')
	parser.add_argument('-o', '--outputfile', dest='outputfile', action='store', default="", help='name of the output file (default: stdout)')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	
	args = parser.parse_args()

	filename = args.inputfile[0]
	f = None
	try:
		f = open(filename, 'r')
	except:
		print("Error: can\'t open input file!")
		return
		
	outputFilename = args.outputfile
	
	lexical_analyser = LexicalAnalyser()
	
	lineIndex = 0
	for line in f:
		line = line.rstrip('\r\n')
		lexical_analyser.analyse_line(lineIndex, line)
		lineIndex = lineIndex + 1
	f.close()
	
	lexical_analyser.save_to_file(outputFilename)
	
########################################################################				 

if __name__ == "__main__":
    main() 



