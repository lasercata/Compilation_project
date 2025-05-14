#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Compiler:
    '''Class managing the generation of the object code'''
    
    # List of object code instructions
    compiled_possible_instructions = [
        "debutProg", "finProg", "reserver", "empiler", "empilerAdresse", "affectation",
        "valeurPile", "get", "put", "moins", "sous", "add", "mult", "div", "egal", "diff",
        "inf", "infegal", "sup", "supeg", "et", "ou", "non", "tra", "tze", "erreur",
        "empilerTas", "empilerIpTas", "empilerAdAt", "reserverBloc", "retourConstr",
        "retourFonct", "retourProc", "empilerParam", "traConstr", "traVirt"
    ]
    
    def __init__(self):
        self.instructions = []
        self.identifiers_count = 0
        self.parameters_count = 0
        
    ################################################################################
    #                                  Instructions manager                        #
    ################################################################################

    def add_instruction(self, name: str, *args):
        '''
        Adding the instruction `name` to the attribute `self.instructions`.

        Args:
            name : the name of the instruction. Should be in self.compiled_possible_instructions, otherwise, a ValueError is thrown.
            *args : the potential arguments of the instruction.
        '''

        if name not in self.compiled_possible_instructions:
            raise ValueError(f'Compiler: add_instruction: name "{name}" is not a known instruction')
    
        self.instructions.append([name, args])
    
    def get_current_address(self) -> int:
        '''Get the current address of the instruction list.'''

        return len(self.instructions) - 1
    
    def set_instruction_args(self, addr: int, arguments: tuple):
        '''
        Set the arguments of the instruction at address `addr` to `arguments`.

        Args:
            addr      : the address of the instruction to modify.
            arguments : the new arguments of the instruction.
        
        Raises:
            ValueError : if the address is out of range.
        '''

        if addr < 0 or addr >= len(self.instructions):
            raise ValueError(f'Compiler: set_instruction_args: address {addr} is out of range')

        self.instructions[addr][1] = arguments
    
    def __str__(self) -> str:
        '''Convert the instruction list to a string usable by the interpretor.'''

        string = ""

        for instruction in self.instructions:
            string += instruction[0] + "("

            for i in range(len(instruction[1])):
                string += str(instruction[1][i])

                if i != len(instruction[1]) - 1:
                    string += ", "

            string += ")\n"

        return string

    ################################################################################
    #                     Memory allocation for identifiers                        #
    ################################################################################

    def new_identifier(self):
        '''
        Increments the identifier count for "reserver" instruction.
        '''

        self.identifiers_count += 1


    def add_reserver_instruction(self):
        '''
        Adds a "reserver" instruction to the instruction list with the current identifier count.
        '''

        self.add_instruction('reserver', self.identifiers_count)
        self.identifiers_count = 0

    ################################################################################
    #                 Parameters count for functions and procedures                #
    ################################################################################

    def new_param(self):
        '''
        Increments the parameter count for "traStat" instruction.
        '''

        self.parameters_count += 1
        
    def add_trastat_instruction(self, ad_p):
        '''
        Adds a "traStat" instruction to the instruction list with the current parameter count.
        '''

        self.add_instruction('traStat', (ad_p,self.parameters_count))
        self.parameters_count = 0
'''
##-Tests
if __name__ == '__main__':
    c = Compiler()
    c.add_instruction('debutProg')
    c.add_instruction('empiler', 3)
    c.add_instruction('finProg')

    print(c.instructions)

    print(c)
'''
