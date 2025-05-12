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


##-Tests
if __name__ == '__main__':
    c = Compiler()
    c.add_instruction('debutProg')
    c.add_instruction('empiler', 3)
    c.add_instruction('finProg')

    print(c.instructions)

    print(c)
