#!/usr/bin/python

'''
@package anasyn
Syntactical Analyser package. 
'''

##-Imports
#---General
import sys, re
import logging

#---Project
try:
    import src.analex as analex

except ModuleNotFoundError:
    import analex

##-Init
logger = logging.getLogger('anasyn')

DEBUG = False
LOGGING_LEVEL = logging.DEBUG


##-Code
class AnaSynException(Exception):
    '''Defines an exception for the syntax analysis'''

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)

########################################################################                     
#### Syntactical Diagrams
########################################################################                     

def program(lexical_analyser: analex.LexicalAnalyser):
    '''
    Entry point of the grammar.

    <program> -> <specifProgPrinc> is <corpsProgPrinc>

    - lexical_analyser : the lexical analyser
    '''

    specifProgPrinc(lexical_analyser)
    lexical_analyser.acceptKeyword("is")
    corpsProgPrinc(lexical_analyser)

def specifProgPrinc(lexical_analyser: analex.LexicalAnalyser):
    '''
    <specifProgPrinc> -> procedure <ident>

    - lexical_analyser : the lexical analyser
    '''

    lexical_analyser.acceptKeyword("procedure")
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of program : " + ident)

def  corpsProgPrinc(lexical_analyser: analex.LexicalAnalyser):
    '''
    <corpsProgPrinc> -> <partieDecla> begin <suiteInstr> end. | begin <suiteInstr> end.

    - lexical_analyser : the lexical analyser
    '''

    if not lexical_analyser.isKeyword("begin"):
        logger.debug("Parsing declarations")
        partieDecla(lexical_analyser)
        logger.debug("End of declarations")

    lexical_analyser.acceptKeyword("begin")

    if not lexical_analyser.isKeyword("end"):
        logger.debug("Parsing instructions")
        suiteInstr(lexical_analyser)
        logger.debug("End of instructions")

    lexical_analyser.acceptKeyword("end")
    lexical_analyser.acceptFel()
    logger.debug("End of program")

def partieDecla(lexical_analyser: analex.LexicalAnalyser):
    '''
    <partieDecla> -> <listeDeclaOp> <listeDeclaVar> | <listeDeclaVar> | <listeDeclaOp>

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
        listeDeclaOp(lexical_analyser)

        if not lexical_analyser.isKeyword("begin"):
            listeDeclaVar(lexical_analyser)

    else:
        listeDeclaVar(lexical_analyser)                

def listeDeclaOp(lexical_analyser: analex.LexicalAnalyser):
    '''
    <listeDeclaOp> -> <declaOp> ; <listeDeclaOp> | <declaOp> ;

    - lexical_analyser : the lexical analyser.
    '''

    declaOp(lexical_analyser)
    lexical_analyser.acceptCharacter(";")

    if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
        listeDeclaOp(lexical_analyser)

def declaOp(lexical_analyser: analex.LexicalAnalyser):
    '''
    <declaOp> -> <fonction> | <procedure>

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isKeyword("procedure"):
        procedure(lexical_analyser)

    if lexical_analyser.isKeyword("function"):
        fonction(lexical_analyser)

def procedure(lexical_analyser: analex.LexicalAnalyser):
    '''
    <procedure> -> procedure <ident> <partieFormelle> is <corpsProc>

    - lexical_analyser : the lexical analyser.
    '''

    lexical_analyser.acceptKeyword("procedure")
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of procedure : "+ident)

    partieFormelle(lexical_analyser)

    lexical_analyser.acceptKeyword("is")
    corpsProc(lexical_analyser)

def fonction(lexical_analyser: analex.LexicalAnalyser):
    '''
    <fonction> -> function <ident> <partieFormelle> return <type> is <corpsFonct>

    - lexical_analyser : the lexical analyser.
    '''

    lexical_analyser.acceptKeyword("function")
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of function : "+ident)

    partieFormelle(lexical_analyser)

    lexical_analyser.acceptKeyword("return")
    nnpType(lexical_analyser)

    lexical_analyser.acceptKeyword("is")
    corpsFonct(lexical_analyser)

def corpsProc(lexical_analyser: analex.LexicalAnalyser):
    '''
    <corpsProc> -> <partieDeclaProc> begin <suiteInstrNonVide> end | begin <suiteInstrNonVide> end

    - lexical_analyser : the lexical analyser.
    '''

    if not lexical_analyser.isKeyword("begin"):
        partieDeclaProc(lexical_analyser)

    lexical_analyser.acceptKeyword("begin")
    suiteInstr(lexical_analyser)
    lexical_analyser.acceptKeyword("end")

def corpsFonct(lexical_analyser: analex.LexicalAnalyser):
    '''
    <corpsFonct> -> <partieDeclaProc> begin <suiteInstrNonVide> end | begin <suiteInstrNonVide> end

    - lexical_analyser : the lexical analyser.
    '''

    if not lexical_analyser.isKeyword("begin"):
        partieDeclaProc(lexical_analyser)

    lexical_analyser.acceptKeyword("begin")
    suiteInstrNonVide(lexical_analyser)
    lexical_analyser.acceptKeyword("end")

def partieFormelle(lexical_analyser: analex.LexicalAnalyser):
    '''
    <partieFormelle> -> ( <listeSpecifFormelles> ) | ()

    - lexical_analyser : the lexical analyser.
    '''

    lexical_analyser.acceptCharacter("(")

    if not lexical_analyser.isCharacter(")"):
        listeSpecifFormelles(lexical_analyser)

    lexical_analyser.acceptCharacter(")")

def listeSpecifFormelles(lexical_analyser: analex.LexicalAnalyser):
    '''
    <listeSpecifFormelles> -> <specif> ; <listeSpecifFormelles> | <specif>

    - lexical_analyser : the lexical analyser.
    '''

    specif(lexical_analyser)

    if not lexical_analyser.isCharacter(")"):
        lexical_analyser.acceptCharacter(";")
        listeSpecifFormelles(lexical_analyser)

def specif(lexical_analyser: analex.LexicalAnalyser):
    '''
    <specif> -> <listeIdent> : <mode> <type> | <listeIdent> : <type>

    - lexical_analyser : the lexical analyser.
    '''

    listeIdent(lexical_analyser)
    lexical_analyser.acceptCharacter(":")

    if lexical_analyser.isKeyword("in"):
        mode(lexical_analyser)

    nnpType(lexical_analyser)

def mode(lexical_analyser: analex.LexicalAnalyser):
    '''
    <mode> -> in | in out

    - lexical_analyser : the lexical analyser.
    '''

    lexical_analyser.acceptKeyword("in")

    if lexical_analyser.isKeyword("out"):
        lexical_analyser.acceptKeyword("out")
        logger.debug("in out parameter")

    else:
        logger.debug("in parameter")

def nnpType(lexical_analyser: analex.LexicalAnalyser):
    '''
    <type> -> integer | boolean

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isKeyword("integer"):
        lexical_analyser.acceptKeyword("integer")
        logger.debug("integer type")

    elif lexical_analyser.isKeyword("boolean"):
        lexical_analyser.acceptKeyword("boolean")
        logger.debug("boolean type")                

    else:
        logger.error("Unknown type found <"+ lexical_analyser.get_value() +">!")
        raise AnaSynException("Unknown type found <"+ lexical_analyser.get_value() +">!")

def partieDeclaProc(lexical_analyser: analex.LexicalAnalyser):
    '''
    <partieDeclaProc> -> <listeDeclaVar>

    - lexical_analyser : the lexical analyser.
    '''

    listeDeclaVar(lexical_analyser)

def listeDeclaVar(lexical_analyser: analex.LexicalAnalyser):
    '''
    <listeDeclaVar> -> <declaVar> <listeDeclaVar> | <declaVar>

    - lexical_analyser : the lexical analyser.
    '''

    declaVar(lexical_analyser)

    if lexical_analyser.isIdentifier():
        listeDeclaVar(lexical_analyser)

def declaVar(lexical_analyser: analex.LexicalAnalyser):
    '''
    <declaVar> -> <listeIdent> : <type> ;

    - lexical_analyser : the lexical analyser.
    '''

    listeIdent(lexical_analyser)
    lexical_analyser.acceptCharacter(":")
    logger.debug("now parsing type...")
    nnpType(lexical_analyser)
    lexical_analyser.acceptCharacter(";")

def listeIdent(lexical_analyser: analex.LexicalAnalyser):
    '''
    <listeIdent> -> <ident>, <listeIdent> | <ident>

    - lexical_analyser : the lexical analyser.
    '''

    ident = lexical_analyser.acceptIdentifier()
    logger.debug("identifier found: "+str(ident))

    if lexical_analyser.isCharacter(","):
        lexical_analyser.acceptCharacter(",")
        listeIdent(lexical_analyser)

def suiteInstrNonVide(lexical_analyser: analex.LexicalAnalyser):
    '''
    <suiteInstrNonVide> -> <instr> ; <suiteInstrNonVide> | <instr>

    - lexical_analyser : the lexical analyser.
    '''

    instr(lexical_analyser)

    if lexical_analyser.isCharacter(";"):
        lexical_analyser.acceptCharacter(";")
        suiteInstrNonVide(lexical_analyser)

def suiteInstr(lexical_analyser: analex.LexicalAnalyser):
    '''
    <suiteInstr> -> <suiteInstrNonVide> | epsilon

    - lexical_analyser : the lexical analyser.
    '''

    if not lexical_analyser.isKeyword("end"):
        suiteInstrNonVide(lexical_analyser)

def instr(lexical_analyser: analex.LexicalAnalyser):        
    '''
    <instr> -> <affectation> | <boucle> | <altern> | <es> | <retour> | <appelProc>

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isKeyword("while"):
        boucle(lexical_analyser)

    elif lexical_analyser.isKeyword("if"):
        altern(lexical_analyser)

    elif lexical_analyser.isKeyword("get") or lexical_analyser.isKeyword("put"):
        es(lexical_analyser)

    elif lexical_analyser.isKeyword("return"):
        retour(lexical_analyser)

    elif lexical_analyser.isIdentifier():
        ident = lexical_analyser.acceptIdentifier()
        if lexical_analyser.isSymbol(":="):                
            # affectation
            lexical_analyser.acceptSymbol(":=")
            expression(lexical_analyser)
            logger.debug("parsed affectation")

        elif lexical_analyser.isCharacter("("):
            lexical_analyser.acceptCharacter("(")

            if not lexical_analyser.isCharacter(")"):
                listePe(lexical_analyser)

            lexical_analyser.acceptCharacter(")")
            logger.debug("parsed procedure call")

        else:
            logger.error("Expecting procedure call or affectation!")
            raise AnaSynException("Expecting procedure call or affectation!")

    else:
        logger.error("Unknown Instruction <"+ lexical_analyser.get_value() +">!")
        raise AnaSynException("Unknown Instruction <"+ lexical_analyser.get_value() +">!")

def listePe(lexical_analyser: analex.LexicalAnalyser):
    '''
    <listePe> -> <expression>, <listePe> | <expression>

    - lexical_analyser : the lexical analyser.
    '''

    expression(lexical_analyser)

    if lexical_analyser.isCharacter(","):
        lexical_analyser.acceptCharacter(",")
        listePe(lexical_analyser)

def expression(lexical_analyser: analex.LexicalAnalyser):
    '''
    <expression> -> <expression> or <exp1> | <exp1>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing expression: " + str(lexical_analyser.get_value()))

    exp1(lexical_analyser)

    if lexical_analyser.isKeyword("or"):
        lexical_analyser.acceptKeyword("or")
        exp1(lexical_analyser)

def exp1(lexical_analyser: analex.LexicalAnalyser):
    '''
    <exp1> -> <exp1> and <exp2> | <exp2>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing exp1")

    exp2(lexical_analyser)

    if lexical_analyser.isKeyword("and"):
        lexical_analyser.acceptKeyword("and")
        exp2(lexical_analyser)

def exp2(lexical_analyser: analex.LexicalAnalyser):
    '''
    <exp2> -> <exp2> <opRel> <exp3> | <exp3>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing exp2")

    exp3(lexical_analyser)

    if (
        lexical_analyser.isSymbol("<") or
        lexical_analyser.isSymbol("<=") or
        lexical_analyser.isSymbol(">") or
        lexical_analyser.isSymbol(">=")
    ):
        opRel(lexical_analyser)
        exp3(lexical_analyser)

    elif lexical_analyser.isSymbol("=") or lexical_analyser.isSymbol("/="): 
        opRel(lexical_analyser)
        exp3(lexical_analyser)

def opRel(lexical_analyser: analex.LexicalAnalyser):
    '''
    <opRel> -> = | /= | < | <= | > | >=

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing relationnal operator: " + lexical_analyser.get_value())

    if lexical_analyser.isSymbol("<"):
        lexical_analyser.acceptSymbol("<")

    elif lexical_analyser.isSymbol("<="):
        lexical_analyser.acceptSymbol("<=")

    elif lexical_analyser.isSymbol(">"):
        lexical_analyser.acceptSymbol(">")

    elif lexical_analyser.isSymbol(">="):
        lexical_analyser.acceptSymbol(">=")

    elif lexical_analyser.isSymbol("="):
        lexical_analyser.acceptSymbol("=")

    elif lexical_analyser.isSymbol("/="):
        lexical_analyser.acceptSymbol("/=")

    else:
        msg = "Unknown relationnal operator <"+ lexical_analyser.get_value() +">!"
        logger.error(msg)
        raise AnaSynException(msg)

def exp3(lexical_analyser: analex.LexicalAnalyser):
    '''
    <exp3> -> <exp3> <opAd> <exp4> | <exp4>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing exp3")
    exp4(lexical_analyser)    

    if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-"):
        opAdd(lexical_analyser)
        exp4(lexical_analyser)

def opAdd(lexical_analyser: analex.LexicalAnalyser):
    '''
    <opAdd> -> + | -

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing additive operator: " + lexical_analyser.get_value())

    if lexical_analyser.isCharacter("+"):
        lexical_analyser.acceptCharacter("+")

    elif lexical_analyser.isCharacter("-"):
        lexical_analyser.acceptCharacter("-")

    else:
        msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
        logger.error(msg)
        raise AnaSynException(msg)

def exp4(lexical_analyser: analex.LexicalAnalyser):
    '''
    <exp4> -> <exp4> <opMult> <prim> | <prim>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing exp4")

    prim(lexical_analyser)    

    if lexical_analyser.isCharacter("*") or lexical_analyser.isCharacter("/"):
        opMult(lexical_analyser)
        prim(lexical_analyser)

def opMult(lexical_analyser: analex.LexicalAnalyser):
    '''
    <opMult> -> * | /

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing multiplicative operator: " + lexical_analyser.get_value())

    if lexical_analyser.isCharacter("*"):
        lexical_analyser.acceptCharacter("*")

    elif lexical_analyser.isCharacter("/"):
        lexical_analyser.acceptCharacter("/")

    else:
        msg = "Unknown multiplicative operator <"+ lexical_analyser.get_value() +">!"
        logger.error(msg)
        raise AnaSynException(msg)

def prim(lexical_analyser: analex.LexicalAnalyser):
    '''
    <prim> -> <opUnaire> <elemPrim> | <elemPrim>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing prim")

    if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-") or lexical_analyser.isKeyword("not"):
        opUnaire(lexical_analyser)

    elemPrim(lexical_analyser)

def opUnaire(lexical_analyser: analex.LexicalAnalyser):
    '''
    <opUnaire> -> + | - | not

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing unary operator: " + lexical_analyser.get_value())

    if lexical_analyser.isCharacter("+"):
        lexical_analyser.acceptCharacter("+")

    elif lexical_analyser.isCharacter("-"):
        lexical_analyser.acceptCharacter("-")

    elif lexical_analyser.isKeyword("not"):
        lexical_analyser.acceptKeyword("not")

    else:
        msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
        logger.error(msg)
        raise AnaSynException(msg)

def elemPrim(lexical_analyser: analex.LexicalAnalyser):
    '''
    <elemPrim> -> <valeur> | ( <expression> ) | <ident> | <appelFonct>

    Note that <appelFonct> is implemented here (and not in a separate function)

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing elemPrim: " + str(lexical_analyser.get_value()))

    if lexical_analyser.isCharacter("("):
        lexical_analyser.acceptCharacter("(")
        expression(lexical_analyser)
        lexical_analyser.acceptCharacter(")")

    elif lexical_analyser.isInteger() or lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
        valeur(lexical_analyser)

    elif lexical_analyser.isIdentifier():
        ident = lexical_analyser.acceptIdentifier()

        if lexical_analyser.isCharacter("("):            # Appel fonct
            lexical_analyser.acceptCharacter("(")

            if not lexical_analyser.isCharacter(")"):
                listePe(lexical_analyser)

            lexical_analyser.acceptCharacter(")")
            logger.debug("parsed procedure call")

            logger.debug("Call to function: " + ident)

        else:
            logger.debug("Use of an identifier as an expression: " + ident)
                        # ...
    else:
        logger.error("Unknown Value!")
        raise AnaSynException("Unknown Value!")

def valeur(lexical_analyser: analex.LexicalAnalyser):
    '''
    <valeur> -> <entier> | <valBool>

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isInteger():
        entier = lexical_analyser.acceptInteger()
        logger.debug("integer value: " + str(entier))
        return "integer"

    elif lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
        vtype = valBool(lexical_analyser)
        return vtype

    else:
        logger.error("Unknown Value! Expecting an integer or a boolean value!")
        raise AnaSynException("Unknown Value ! Expecting an integer or a boolean value!")

def valBool(lexical_analyser: analex.LexicalAnalyser):
    '''
    <valBool> -> true | false

    - lexical_analyser : the lexical analyser.
    '''

    if lexical_analyser.isKeyword("true"):
        lexical_analyser.acceptKeyword("true")    
        logger.debug("boolean true value")

    else:
        logger.debug("boolean false value")
        lexical_analyser.acceptKeyword("false")

    return "boolean"

def es(lexical_analyser: analex.LexicalAnalyser):
    '''
    <es> -> get ( <ident> ) | put ( <expression> )

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing E/S instruction: " + lexical_analyser.get_value())

    if lexical_analyser.isKeyword("get"):
        lexical_analyser.acceptKeyword("get")
        lexical_analyser.acceptCharacter("(")
        ident = lexical_analyser.acceptIdentifier()
        lexical_analyser.acceptCharacter(")")
        logger.debug("Call to get "+ident)

    elif lexical_analyser.isKeyword("put"):
        lexical_analyser.acceptKeyword("put")
        lexical_analyser.acceptCharacter("(")
        expression(lexical_analyser)
        lexical_analyser.acceptCharacter(")")
        logger.debug("Call to put")

    else:
        logger.error("Unknown E/S instruction!")
        raise AnaSynException("Unknown E/S instruction!")

def boucle(lexical_analyser: analex.LexicalAnalyser):
    '''
    <boucle> -> while <expression> loop <suiteInstr> end

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing while loop: ")
    lexical_analyser.acceptKeyword("while")

    expression(lexical_analyser)

    lexical_analyser.acceptKeyword("loop")
    suiteInstr(lexical_analyser)

    lexical_analyser.acceptKeyword("end")
    logger.debug("end of while loop ")

def altern(lexical_analyser: analex.LexicalAnalyser):
    '''
    <altern> -> if <expression> then <suiteInstr> end | if <expression> then <suiteInstr> else <suiteInstr> end

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing if: ")
    lexical_analyser.acceptKeyword("if")

    expression(lexical_analyser)

    lexical_analyser.acceptKeyword("then")
    suiteInstr(lexical_analyser)

    if lexical_analyser.isKeyword("else"):
        lexical_analyser.acceptKeyword("else")
        suiteInstr(lexical_analyser)

    lexical_analyser.acceptKeyword("end")
    logger.debug("end of if")

def retour(lexical_analyser: analex.LexicalAnalyser):
    '''
    <retour> -> return <expression>

    - lexical_analyser : the lexical analyser.
    '''

    logger.debug("parsing return instruction")
    lexical_analyser.acceptKeyword("return")
    expression(lexical_analyser)



########################################################################
def main_anasyn(fn: str, fn_out: str, pseudo_code: bool, show_ident_table: bool, debug_lvl):
    '''
    TODO: Docstring for main_anasyn.

    - fn               : the input filename of the program ;
    - fn_out           : the name of the potential output file. If "", prints to stdout instead ;
    - pseudo_code      : TODO
    - show_ident_table : if true, displays the ident table ;
    - debug_lvl        : indicates the logging level.
    '''

    # create logger
    LOGGING_LEVEL = debug_lvl
    logger.setLevel(LOGGING_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(LOGGING_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if pseudo_code: #TODO
        True#

    else:
        False#

    lexical_analyser = analex.LexicalAnalyser()

    try:
        with open(fn, 'r') as f:
            lineIndex = 0

            for line in f:
                line = line.rstrip('\r\n')
                lexical_analyser.analyse_line(lineIndex, line)
                lineIndex = lineIndex + 1

    except Exception as e:
        print(f"Error: {e}: can't open the input file!")
        return

    # launch the analysis of the program
    try:
        lexical_analyser.init_analyser()
        program(lexical_analyser)

    except Exception as err:
        print(f'Syntax error: {err}')

    if show_ident_table:
        print("------ IDENTIFIER TABLE ------")
        #print(str(identifierTable))
        print("------ END OF IDENTIFIER TABLE ------")


    if fn_out != '':
        try:
            output_file = open(fn_out, 'w')

        except:
            print("Error: can't open output file!")
            return

    else:
        output_file = sys.stdout

    # Outputs the generated code to a file
    #instrIndex = 0
    #while instrIndex < codeGenerator.get_instruction_counter():
    #        output_file.write("%s\n" % str(codeGenerator.get_instruction_at_index(instrIndex)))
    #        instrIndex += 1

    if fn_out != '':
        output_file.close() 

########################################################################

if __name__ == "__main__":
    pass # To run this file, use the file `main`.
