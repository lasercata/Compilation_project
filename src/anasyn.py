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
import src.analex as analex
import src.compiler as compiler
from src.utils import get_logger
from src.idtable import IdentifierTable, IdentifierCarac, IdentifierType

##-Code
class AnaSynException(Exception):
    '''Defines an exception for the syntax analysis'''

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)

class SemanticException(Exception):
    '''Defines an exception for semantic error'''

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)

########################################################################                     
#### Syntactical Diagrams
########################################################################                     

class Grammar:
    '''
    Class implementing the grammar rules.

    It checks the correctness of the input program and compiles it to object code using `compiler`.
    '''

    def __init__(self, src_code: str, debug_lvl: int = logging.INFO):
        '''
        Instanciates the class.

        Args:
            src_code (str): the source code, as a string
            debug_lvl (int): the debug level
        '''

        #---Create the lexical analyser
        self.create_lexical_analyser(src_code)

        #---Create the compiler
        self.comp = compiler.Compiler()

        #---Create the id table
        self.id_table = IdentifierTable()

        #---Set up self.logger
        self.logger = get_logger('ANASYN', debug_lvl)
        
        #---Set up the scope
        self.current_scope = "global"
        
        #---Set up the identifier        
        self.current_function_name = None


    def create_lexical_analyser(self, src_code: str):
        '''Creates the lexical analyser.'''

        self.lexical_analyser = analex.LexicalAnalyser()

        lineIndex = 0
        for line in src_code.split('\n'):
            line = line.rstrip('\r\n')
            self.lexical_analyser.analyse_line(lineIndex, line)
            lineIndex = lineIndex + 1


    #===Grammar rules
    def program(self):
        '''
        Entry point of the grammar.

        <program> -> <specifProgPrinc> is <corpsProgPrinc>
        '''

        # Point de génération de code : Début du programme
        self.comp.add_instruction('debutProg')

        self.specifProgPrinc()
        self.lexical_analyser.acceptKeyword("is")
        self.corpsProgPrinc()

        self.comp.add_instruction('finProg')

    def specifProgPrinc(self):
        '''
        <specifProgPrinc> -> procedure <ident>
        '''

        self.lexical_analyser.acceptKeyword("procedure")
        ident = self.lexical_analyser.acceptIdentifier()

        self.logger.debug("Name of program : " + ident)
        
    def  corpsProgPrinc(self):
        '''
        <corpsProgPrinc> -> <partieDecla> begin <suiteInstr> end. | begin <suiteInstr> end.
        '''

        if not self.lexical_analyser.isKeyword("begin"):
            self.logger.debug("Parsing declarations")
            self.partieDecla()
    
                
            self.logger.debug("End of declarations")

        self.lexical_analyser.acceptKeyword("begin")

        if not self.lexical_analyser.isKeyword("end"):
            self.logger.debug("Parsing instructions")
            self.suiteInstr()
            self.logger.debug("End of instructions")

        self.lexical_analyser.acceptKeyword("end")
        for nom, carac in self.id_table.tbl.items():
                if carac.type in (IdentifierType.PROCEDURE, IdentifierType.FUNCTION) and carac.address is None:
                    self.id_table.assign_procedure_address(nom)
        self.lexical_analyser.acceptFel()
        self.logger.debug("End of program")

    def partieDecla(self):
        '''
        <partieDecla> -> <listeDeclaOp> <listeDeclaVar> | <listeDeclaVar> | <listeDeclaOp>.
        '''

        if self.lexical_analyser.isKeyword("procedure") or self.lexical_analyser.isKeyword("function") :
            self.comp.add_instruction('tra', None)
            tra_addr = self.comp.get_current_address()
            self.listeDeclaOp()
            self.comp.set_instruction_args(tra_addr, (self.comp.get_current_address() + 2,))

            if not self.lexical_analyser.isKeyword("begin"):
                self.listeDeclaVar()
            
        else:
            self.listeDeclaVar()                

    def listeDeclaOp(self):
        '''
        <listeDeclaOp> -> <declaOp> ; <listeDeclaOp> | <declaOp> ;.
        '''

        self.declaOp()
        self.lexical_analyser.acceptCharacter(";")

        if self.lexical_analyser.isKeyword("procedure") or self.lexical_analyser.isKeyword("function") :
            self.listeDeclaOp()

    def declaOp(self):
        '''
        <declaOp> -> <fonction> | <procedure>.
        '''

        if self.lexical_analyser.isKeyword("procedure"):
            self.id_table.addr_param = 0 #Reset the parameter address counter
            self.id_table.addr_local = 0 #Reset the local address counter
            self.procedure()

        if self.lexical_analyser.isKeyword("function"):
            self.id_table.addr_param = 0 #Reset the parameter address counter
            self.id_table.addr_local = 0 #Reset the local address counter
            self.fonction()

    def procedure(self):
        '''
        <procedure> -> procedure <ident> <partieFormelle> is <corpsProc>.
        '''

        self.lexical_analyser.acceptKeyword("procedure")
        self.current_scope = "global" #Procedure's scope
        ident = self.lexical_analyser.acceptIdentifier()
        
        self.current_function_name = ident #Set the current function name for later use

        self.comp.add_trastat_adress(ident,self.comp.get_current_address()+2)

        self.logger.debug("Name of procedure : " + ident)
        carac = IdentifierCarac(IdentifierType.PROCEDURE, ident, self.current_scope)
        self.id_table.addIdentifier(ident, carac) #Ajout dans la table des identificateurs
                
        self.current_scope = "parameter" #procedure's parameters' scope
        self.partieFormelle()

        self.current_scope = "local" #Scope des variables locales
        self.lexical_analyser.acceptKeyword("is")
        
        self.corpsProc()
        self.comp.add_instruction('retourProc')
        
        self.current_scope = "global" #Scope remis à global pour le programme principal

    def fonction(self):
        '''
        <fonction> -> function <ident> <partieFormelle> return <type> is <corpsFonct>.
        '''
        entry_address = self.comp.get_current_address() + 1
        
        self.lexical_analyser.acceptKeyword("function")
        ident = self.lexical_analyser.acceptIdentifier()
        self.comp.add_trastat_adress(ident, self.comp.get_current_address() + 2)
        self.logger.debug("Name of function : " + ident)
        self.current_scope = "global" #Function's scope
        carac = IdentifierCarac(IdentifierType.FUNCTION, ident, self.current_scope)
        carac.adress = entry_address
        self.id_table.addIdentifier(ident, carac) #Add in the identifier table
        
        self.current_scope = "parameter" #function's parameters' scope
        self.partieFormelle()

        self.lexical_analyser.acceptKeyword("return")
        self.nnpType()

        self.current_scope = "local" #local variables' scope
        self.lexical_analyser.acceptKeyword("is")
        entry_addr = self.comp.get_current_address() + 1 #Address of the function entry point
        self.corpsFonct()

        self.current_scope = "global" #reset the scope to global for the main program

    def corpsProc(self):
        '''
        <corpsProc> -> <partieDeclaProc> begin <suiteInstrNonVide> end | begin <suiteInstrNonVide> end.
        '''

        if not self.lexical_analyser.isKeyword("begin"):
            self.current_scope = "local" #Scope de la procédure
            self.partieDeclaProc()

        self.lexical_analyser.acceptKeyword("begin")
        self.suiteInstr()
        self.lexical_analyser.acceptKeyword("end")

    def corpsFonct(self):
        '''
        <corpsFonct> -> <partieDeclaProc> begin <suiteInstrNonVide> end | begin <suiteInstrNonVide> end.
        '''

        if not self.lexical_analyser.isKeyword("begin"):
            self.current_scope = "local" #Scope de la fonction
            self.partieDeclaProc()

        self.lexical_analyser.acceptKeyword("begin")
        self.suiteInstrNonVide()
        self.lexical_analyser.acceptKeyword("end")

    def partieFormelle(self):
        '''
        <partieFormelle> -> ( <listeSpecifFormelles> ) | ().
        '''

        self.lexical_analyser.acceptCharacter("(")

        if not self.lexical_analyser.isCharacter(")"):
            self.listeSpecifFormelles()

        self.lexical_analyser.acceptCharacter(")")

    def listeSpecifFormelles(self):
        '''
        <listeSpecifFormelles> -> <specif> ; <listeSpecifFormelles> | <specif>.
        '''

        self.specif()

        if not self.lexical_analyser.isCharacter(")"):
            self.lexical_analyser.acceptCharacter(";")
            self.listeSpecifFormelles()

    def specif(self):
        '''
        <specif> -> <listeIdent> : <mode> <type> | <listeIdent> : <type>.
        '''

        # self.listeIdent()
        self.current_scope = "parameter" #Scope de la variable du programme principal
        self.listeIdentParam()
        self.lexical_analyser.acceptCharacter(":")

        if self.lexical_analyser.isKeyword("in"):
            self.mode()
        
        else:
            self.logger.debug("implicit 'in' parameter (default mode)")
            for key, value in self.id_table.tbl.items():
                if value.scope == "parameter" and value.type == "NONE":
                    value.isIn = True
                    value.isOut = False
                    value.scope = "local"  # Comme tout paramètre 'in' par valeur

        self.nnpType()

    def mode(self):
        '''
        <mode> -> in | in out.
        '''

        self.lexical_analyser.acceptKeyword("in")

        if self.lexical_analyser.isKeyword("out"):
            self.lexical_analyser.acceptKeyword("out")

            self.logger.debug("in out parameter")
            for key, value in self.id_table.tbl.items():
                if value.scope == "parameter":
                    value.isIn = True
                    value.isOut = True
                    value.scope = "parameter"

        else:
            self.logger.debug("in parameter")
            for key, value in self.id_table.tbl.items():
                if value.scope == "parameter":
                    value.isIn = True
                    value.isOut = False
                    value.scope = "local"

    def nnpType(self):
        '''
        <type> -> integer | boolean.
        '''

        if self.lexical_analyser.isKeyword("integer"):
            self.lexical_analyser.acceptKeyword("integer")

            self.logger.debug("integer type")
            for key, value in self.id_table.tbl.items():
                if value.type == "NONE":
                    # self.id_table.tbl[key].type = "integer"
                    value.type = "integer"

        elif self.lexical_analyser.isKeyword("boolean"):
            self.lexical_analyser.acceptKeyword("boolean")

            self.logger.debug("boolean type")
            for key, value in self.id_table.tbl.items():
                if value.type == "NONE":
                    # self.id_table.tbl[key].type = "boolean" 
                    value.type = "boolean"

        else:
            self.logger.error("Unknown type found <" + self.lexical_analyser.get_value() + ">!")
            raise AnaSynException("Unknown type found <" + self.lexical_analyser.get_value() + ">!")

    def partieDeclaProc(self):
        '''
        <partieDeclaProc> -> <listeDeclaVar>.
        '''

        self.listeDeclaVar()

    def listeDeclaVar(self):
        '''
        <listeDeclaVar> -> <declaVar> <listeDeclaVar> | <declaVar>.
        '''

        self.declaVar()

        if self.lexical_analyser.isIdentifier():
            self.listeDeclaVar()

    def declaVar(self):
        '''
        <declaVar> -> <listeIdent> : <type> ;.
        '''
        self.listeIdent()
        self.comp.add_reserver_instruction()
        self.lexical_analyser.acceptCharacter(":")
        self.logger.debug("now parsing type...")
        self.nnpType()
        self.lexical_analyser.acceptCharacter(";")

    def listeIdent(self):
        '''
        <listeIdent> -> <ident>, <listeIdent> | <ident>.
        '''

        ident = self.lexical_analyser.acceptIdentifier()
        self.logger.debug("identifier found: "+str(ident))
        self.id_table.addIdentifier(ident, IdentifierCarac("NONE", ident, self.current_scope)) #Ajout dans la table des identificateurs
        
        self.comp.new_identifier()

        if self.lexical_analyser.isCharacter(","):
            self.lexical_analyser.acceptCharacter(",")
            self.listeIdent()   

    def listeIdentParam(self):
        '''
        TODO: description   
        '''

        param_ident = self.lexical_analyser.acceptIdentifier()

        self.logger.debug("identifier found: " + str(param_ident))
        self.current_scope = "parameter" #procedure's parameters' scope
        self.id_table.addIdentifier(param_ident, IdentifierCarac("NONE", param_ident, self.current_scope)) #add in the identifier table
        
        if self.lexical_analyser.isCharacter(","):
            self.lexical_analyser.acceptCharacter(",")
            self.listeIdentParam()
 

    def suiteInstrNonVide(self):
        '''
        <suiteInstrNonVide> -> <instr> ; <suiteInstrNonVide> | <instr>.
        '''

        self.instr()

        if self.lexical_analyser.isCharacter(";"):
            self.lexical_analyser.acceptCharacter(";")
            self.suiteInstrNonVide()

    def suiteInstr(self):
        '''
        <suiteInstr> -> <suiteInstrNonVide> | epsilon.
        '''

        if not self.lexical_analyser.isKeyword("end"):
            self.suiteInstrNonVide()

    def instr(self):
        '''
        <instr> -> <affectation> | <boucle> | <altern> | <es> | <retour> | <appelProc>.
        '''

        if self.lexical_analyser.isKeyword("while"):
            self.boucle()

        elif self.lexical_analyser.isKeyword("if"):
            self.altern()

        elif self.lexical_analyser.isKeyword("get") or self.lexical_analyser.isKeyword("put"):
            self.es()

        elif self.lexical_analyser.isKeyword("return"):
            self.retour()

        elif self.lexical_analyser.isIdentifier():
            ident = self.lexical_analyser.acceptIdentifier()

            if self.lexical_analyser.isSymbol(":="):                
                # affectation
                self.lexical_analyser.acceptSymbol(":=")

                var_name = self.lexical_analyser.lexical_units[self.lexical_analyser.lexical_unit_index - 2].value
                var = self.id_table.tbl[var_name]
                var_static_addr = var.address

                # print(var_name + " is a " + var_scope)

                var_type = var.type
                val = self.lexical_analyser.lexical_units[self.lexical_analyser.lexical_unit_index]

                if (
                    (var_type == IdentifierType.INTEGER and type(val) not in (analex.Integer, analex.Identifier))
                    # or (var_type == IdentifierType.BOOLEAN and type(val) != analex.Keyword)
                ):
                    raise SemanticException('affectation: wrong type')

                var_scope = var.scope
                if var_scope == "parameter":
                    self.comp.add_instruction('empilerParam', var_static_addr)
                elif var_scope == "local":
                    self.comp.add_instruction('empilerAd', var_static_addr)
                else:
                    self.comp.add_instruction('empiler', var_static_addr)

                self.expression()
                self.comp.add_instruction('affectation')
                self.logger.debug("parsed affectation")

            elif self.lexical_analyser.isCharacter("("):
                self.comp.add_instruction('reserverBloc')
                self.lexical_analyser.acceptCharacter("(")
                
                if not self.lexical_analyser.isCharacter(")"):
                    self.listePe()

                self.lexical_analyser.acceptCharacter(")")
                self.logger.debug("parsed procedure call")
                address_proc_func = self.comp.traStat_memory[ident]
                self.comp.add_trastat_instruction(address_proc_func)

            else:
                self.logger.error("Expecting procedure call or affectation!")
                raise AnaSynException("Expecting procedure call or affectation!")

        else:
            self.logger.error("Unknown Instruction <"+ self.lexical_analyser.get_value() +">!")
            raise AnaSynException("Unknown Instruction <"+ self.lexical_analyser.get_value() +">!")

    def listePe(self):
        '''
        <listePe> -> <expression>, <listePe> | <expression>.
        '''

        self.expression()
        self.comp.new_param()
        if self.lexical_analyser.isCharacter(","):
            self.lexical_analyser.acceptCharacter(",")
            self.listePe()

    def expression(self):
        '''
        <expression> -> <expression> or <exp1> | <exp1>.
        '''

        self.logger.debug("parsing expression: " + str(self.lexical_analyser.get_value()))

        self.exp1()

        if self.lexical_analyser.isKeyword("or"):
            self.lexical_analyser.acceptKeyword("or")
            self.exp1()
            self.comp.add_instruction("ou")

    def exp1(self):
        '''
        <exp1> -> <exp1> and <exp2> | <exp2>.
        '''

        self.logger.debug("parsing exp1")

        self.exp2()

        if self.lexical_analyser.isKeyword("and"):
            self.lexical_analyser.acceptKeyword("and")
            self.exp2()
            self.comp.add_instruction("et")

    def exp2(self):
        '''
        <exp2> -> <exp2> <opRel> <exp3> | <exp3>.
        '''

        self.logger.debug("parsing exp2")

        self.exp3()

        if (
            self.lexical_analyser.isSymbol("<") or
            self.lexical_analyser.isSymbol("<=") or
            self.lexical_analyser.isSymbol(">") or
            self.lexical_analyser.isSymbol(">=")
        ):
            operator = self.opRel()
            self.exp3()
            self.comp.add_instruction(operator)

        elif self.lexical_analyser.isSymbol("=") or self.lexical_analyser.isSymbol("/="): 
            operator = self.opRel()
            self.exp3()
            self.comp.add_instruction(operator)

    def opRel(self):
        '''
        <opRel> -> = | /= | < | <= | > | >=.
        '''

        self.logger.debug("parsing relationnal operator: " + self.lexical_analyser.get_value())

        if self.lexical_analyser.isSymbol("<"):
            self.lexical_analyser.acceptSymbol("<")
            return 'inf'

        elif self.lexical_analyser.isSymbol("<="):
            self.lexical_analyser.acceptSymbol("<=")
            return 'infeg'

        elif self.lexical_analyser.isSymbol(">"):
            self.lexical_analyser.acceptSymbol(">")
            return 'sup'

        elif self.lexical_analyser.isSymbol(">="):
            self.lexical_analyser.acceptSymbol(">=")
            return 'supeg'

        elif self.lexical_analyser.isSymbol("="):
            self.lexical_analyser.acceptSymbol("=")
            return 'egal'

        elif self.lexical_analyser.isSymbol("/="):
            self.lexical_analyser.acceptSymbol("/=")
            return 'diff'

        else:
            msg = "Unknown relationnal operator <"+ self.lexical_analyser.get_value() +">!"
            self.logger.error(msg)
            raise AnaSynException(msg)

    def exp3(self):
        '''
        <exp3> -> <exp3> <opAd> <exp4> | <exp4>.
        '''

        self.logger.debug("parsing exp3")
        self.exp4()    

        if self.lexical_analyser.isCharacter("+") or self.lexical_analyser.isCharacter("-"):
            operator = self.opAdd()
            self.exp4()
            self.comp.add_instruction(operator)

    def opAdd(self):
        '''
        <opAdd> -> + | -.
        '''

        self.logger.debug("parsing additive operator: " + self.lexical_analyser.get_value())

        if self.lexical_analyser.isCharacter("+"):
            self.lexical_analyser.acceptCharacter("+")
            return 'add'

        elif self.lexical_analyser.isCharacter("-"):
            self.lexical_analyser.acceptCharacter("-")
            return 'sous'

        else:
            msg = "Unknown additive operator <"+ self.lexical_analyser.get_value() +">!"
            self.logger.error(msg)
            raise AnaSynException(msg)

    def exp4(self):
        '''
        <exp4> -> <exp4> <opMult> <prim> | <prim>.
        '''

        self.logger.debug("parsing exp4")

        self.prim()    

        if self.lexical_analyser.isCharacter("*") or self.lexical_analyser.isCharacter("/"):
            operator = self.opMult()
            self.prim()
            self.comp.add_instruction(operator)

    def opMult(self):
        '''
        <opMult> -> * | /.
        '''

        self.logger.debug("parsing multiplicative operator: " + self.lexical_analyser.get_value())

        if self.lexical_analyser.isCharacter("*"):
            self.lexical_analyser.acceptCharacter("*")
            return 'mult'

        elif self.lexical_analyser.isCharacter("/"):
            self.lexical_analyser.acceptCharacter("/")
            return 'div'

        else:
            msg = "Unknown multiplicative operator <"+ self.lexical_analyser.get_value() +">!"
            self.logger.error(msg)
            raise AnaSynException(msg)

    def prim(self):
        '''
        <prim> -> <opUnaire> <elemPrim> | <elemPrim>.
        '''

        self.logger.debug("parsing prim")

        if self.lexical_analyser.isCharacter("+") or self.lexical_analyser.isCharacter("-") or self.lexical_analyser.isKeyword("not"):
            operator = self.opUnaire()
            self.elemPrim()
            self.comp.add_instruction(operator)
        else :
            self.elemPrim()


    def opUnaire(self):
        '''
        <opUnaire> -> + | - | not.
        '''

        self.logger.debug("parsing unary operator: " + self.lexical_analyser.get_value())

        if self.lexical_analyser.isCharacter("+"):
            self.lexical_analyser.acceptCharacter("+")

        elif self.lexical_analyser.isCharacter("-"):
            self.lexical_analyser.acceptCharacter("-")
            return 'moins'

        elif self.lexical_analyser.isKeyword("not"):
            self.lexical_analyser.acceptKeyword("not")
            return 'non'

        else:
            msg = "Unknown additive operator <"+ self.lexical_analyser.get_value() +">!"
            self.logger.error(msg)
            raise AnaSynException(msg)

    def elemPrim(self):
        '''
        <elemPrim> -> <valeur> | ( <expression> ) | <ident> | <appelFonct>

        Note that <appelFonct> is implemented here (and not in a separate function).
        '''

        self.logger.debug("parsing elemPrim: " + str(self.lexical_analyser.get_value()))

        if self.lexical_analyser.isCharacter("("):
            self.lexical_analyser.acceptCharacter("(")
            self.expression()
            self.lexical_analyser.acceptCharacter(")")

        elif self.lexical_analyser.isInteger() or self.lexical_analyser.isKeyword("true") or self.lexical_analyser.isKeyword("false"):
            self.valeur()

        elif self.lexical_analyser.isIdentifier():
            ident = self.lexical_analyser.acceptIdentifier()

            if self.lexical_analyser.isCharacter("("):            # Appel fonct
                self.comp.add_instruction('reserverBloc')
                self.lexical_analyser.acceptCharacter("(")

                if not self.lexical_analyser.isCharacter(")"):
                    self.listePe()

                self.lexical_analyser.acceptCharacter(")")
                self.logger.debug("parsed procedure call")
                address_proc_func = self.comp.traStat_memory[ident]
                self.comp.add_trastat_instruction(address_proc_func)

                self.logger.debug("Call to function: " + ident)

            else:
                self.logger.debug("Use of an identifier as an expression: " + ident)

                var_name = self.lexical_analyser.lexical_units[self.lexical_analyser.lexical_unit_index - 1].value
                var_static_addr = self.id_table.tbl[var_name].address
                var_scope = self.id_table.tbl[var_name].scope

                if var_scope == "parameter":
                    self.comp.add_instruction('empilerParam', var_static_addr)
                elif var_scope == "local":
                    self.comp.add_instruction('empilerAd', var_static_addr)
                else :
                    self.comp.add_instruction('empiler', var_static_addr)
                self.comp.add_instruction('valeurPile')
        else:
            self.logger.error("Unknown Value!")
            raise AnaSynException("Unknown Value!")

    def valeur(self):
        '''
        <valeur> -> <entier> | <valBool>.
        '''

        if self.lexical_analyser.isInteger():
            entier = self.lexical_analyser.acceptInteger()
            self.logger.debug("integer value: " + str(entier))
            self.comp.add_instruction("empiler", entier)
            return "integer"

        elif self.lexical_analyser.isKeyword("true") or self.lexical_analyser.isKeyword("false"):
            vtype = self.valBool()
            return vtype

        else:
            self.logger.error("Unknown Value! Expecting an integer or a boolean value!")
            raise AnaSynException("Unknown Value ! Expecting an integer or a boolean value!")

    def valBool(self):
        '''
        <valBool> -> true | false.
        '''

        if self.lexical_analyser.isKeyword("true"):
            self.lexical_analyser.acceptKeyword("true")    
            self.logger.debug("boolean true value")
            self.comp.add_instruction("empiler", 1)

        else:
            self.logger.debug("boolean false value")
            self.lexical_analyser.acceptKeyword("false")
            self.comp.add_instruction("empiler", 0)

        return "boolean"

    def es(self):
        '''
        <es> -> get ( <ident> ) | put ( <expression> ).
        '''

        self.logger.debug("parsing E/S instruction: " + self.lexical_analyser.get_value())

        if self.lexical_analyser.isKeyword("get"):
            self.lexical_analyser.acceptKeyword("get")

            self.lexical_analyser.acceptCharacter("(")
            ident = self.lexical_analyser.acceptIdentifier()
            self.lexical_analyser.acceptCharacter(")")

            ident_addr = self.id_table.tbl[ident].address
            self.comp.add_instruction('empiler', ident_addr)
            self.comp.add_instruction('get')
            self.logger.debug("Call to get "+ident)

            if self.id_table.tbl[ident].type != IdentifierType.INTEGER:
                raise SemanticException('get takes an integer')

        elif self.lexical_analyser.isKeyword("put"):
            self.lexical_analyser.acceptKeyword("put")

            self.lexical_analyser.acceptCharacter("(")
            self.expression()
            self.lexical_analyser.acceptCharacter(")")

            self.comp.add_instruction('put')
            self.logger.debug("Call to put")

            #TODO: semantic error if expression is not an int
            # if self.id_table.tbl[ident].type != IdentifierType.INTEGER:
            #     raise SemanticException('get takes an integer')

        else:
            self.logger.error("Unknown E/S instruction!")
            raise AnaSynException("Unknown E/S instruction!")

    def boucle(self):
        '''
        <boucle> -> while <expression> loop <suiteInstr> end.
        '''

        self.logger.debug("parsing while loop: ")
        self.lexical_analyser.acceptKeyword("while")

        # Compiling the beginning of the while loop (condition)
        ad1 = self.comp.get_current_address() + 1 # ad1
        self.expression() # compile condition
        
        self.lexical_analyser.acceptKeyword("loop")
        
        # Adding tze jump, with a placeholder for the address
        self.comp.add_instruction('tze', None)
        tze_addr = self.comp.get_current_address()
        
        # Compiling the loop body
        self.suiteInstr()
        
        self.comp.add_instruction("tra", ad1 + 1)
        ad2 = self.comp.get_current_address() + 2
        self.comp.set_instruction_args(tze_addr, (ad2,))

        self.lexical_analyser.acceptKeyword("end")
        self.logger.debug("end of while loop ")

    def altern(self):
        '''
        <altern> -> if <expression> then <suiteInstr> end | if <expression> then <suiteInstr> else <suiteInstr> end.
        '''

        self.logger.debug("parsing if: ")
        self.lexical_analyser.acceptKeyword("if")

        self.expression()
        
        # Adding tze jump, with a placeholder for the address
        self.comp.add_instruction('tze', None)
        tze_addr = self.comp.get_current_address()
        
        self.lexical_analyser.acceptKeyword("then")
        self.suiteInstr()
        
        ad1 = self.comp.get_current_address() + 1


        if self.lexical_analyser.isKeyword("else"):
            self.lexical_analyser.acceptKeyword("else")
            
            # Adding tra jump
            self.comp.add_instruction('tra', None)
            tra_addr = self.comp.get_current_address()
        
            # Modifying the tze parameter
            ad1 += 1
            self.comp.set_instruction_args(tze_addr, (ad1 + 1,))
            
            self.suiteInstr()
            
            ad2 = self.comp.get_current_address() + 1
            self.comp.set_instruction_args(tra_addr, (ad2 + 1,))

        else:
            self.comp.set_instruction_args(tze_addr, (ad1 + 1,))

        self.lexical_analyser.acceptKeyword("end")
        self.logger.debug("end of if")

    def retour(self):
        '''
        <retour> -> return <expression>.
        '''

        self.logger.debug("parsing return instruction")
        self.lexical_analyser.acceptKeyword("return")
        self.expression()
        self.comp.add_instruction('retourFonct')

    #===Compile
    def compile(self, show_ident_table: bool = False) -> str:
        '''
        Compiles the NNP source code to NNP object code.

        If an exception occurs, it throws a `SyntaxError`.

        Args:
            :show_ident_table: if True, prints the identifier table.
        '''

        try:
            self.lexical_analyser.init_analyser()
            self.program()

            if show_ident_table:
                print("------ IDENTIFIER TABLE ------")
                self.id_table.printTable()
                print("------ END OF IDENTIFIER TABLE ------")

        except Exception as err:
            raise SyntaxError(err)

        return str(self.comp)


########################################################################
def main_anasyn(file_content: str, fn_out: str, show_ident_table: bool, debug_lvl):
    '''
    TODO: Docstring for main_anasyn.

    - file_content     : the content of the file (the NNP program) ;
    - fn_out           : the name of the potential output file. If "", prints to stdout instead ;
    - show_ident_table : if true, displays the ident table ;
    - debug_lvl        : indicates the logging level.
    '''

    #---Run the analysis
    G = Grammar(file_content, debug_lvl)

    try:
        instructions_str = G.compile(show_ident_table)

    except SyntaxError as err:
        print(f'Syntax error: {err}')
        return

    #---Write to file / stdout
    #-Select file or stdout
    if fn_out != '':
        try:
            output_file = open(fn_out, 'w')

        except:
            print("Error: can't open output file!")
            return

    else:
        output_file = sys.stdout

    #-Write
    if instructions_str != '':
        output_file.write(instructions_str)

        if debug_lvl == logging.DEBUG:
            print(f'Output to file: "{fn_out}"')

    else:
        if debug_lvl == logging.DEBUG:
            print('No instruction generated!')
            
    #-Close file
    if fn_out != '':
        output_file.close()


########################################################################

if __name__ == "__main__":
    pass # To run this file, use the file `main`.
