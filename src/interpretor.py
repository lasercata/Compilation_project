import sys 

class VM: 
    '''Class defining the interpretor of the object code.'''

    def __init__(self, object_code: str):
        '''
        Constructor

        - object_code : the instructions (in object nilnovi).
        '''

        self.instructions = object_code.split('\n')

    def pop_stack(self) -> None | int | bool:
        '''
        Removes the top element of the stack.
        '''
    
        ret = self.stack[self.ip]
        del self.stack[self.ip]
        self.ip -= 1

        return ret

    def run(self, debug: bool = False):
        '''Runs the program.'''

        self.debutProg()
        self.co = 0
    
        last_line = len(self.instructions)

        while self.co < last_line:
            inst = self.instructions[self.co]
            parsed_instr = parse_nilnovi_object_line(inst)

            if debug:
                print(parsed_instr)
                print(self.stack)

            self.execute_instruction(parsed_instr)
            self.co += 1
       

    def debutProg(self):
        self.stack = []
        self.dictVariable = {}
        self.ip = -1 #Increment
        self.ipTas = -1 #Decrement
        self.base = 0


    def finProg(self):
        raise Exception('Program ended')

    def reserver(self, n: int):
        '''Reserve n places, supposed the heap was far away from the stack '''

        for _ in range(0, n):
            self.stack.insert(self.ip + 1, None)

        self.ip += n

    def empiler(self, val: int):
        self.reserver(1)
        self.stack[self.ip]=val

    def empilerAd(self, addr: int):
        self.empiler(self.stack[addr])

   # def _affectation(self, varName: str, varValue: int):
   #     self.dictVariable[varName] = varValue #self.stack[self.stack.index(None)-2]=self.stack[self.stack.index(null)-1]
    
    def affectation(self):
        self.stack[self.stack[self.ip - 1]]= self.stack[self.ip]
        self.pop_stack()
        self.pop_stack()

    def valeurPile(self):
        self.stack[self.ip] = self.stack[self.stack[self.ip]]

    def get(self):
        self.stack[self.stack[self.ip]] = input(">")

    def put(self):
        '''ça put et ça dépile aussi'''
        print(self.stack[self.ip])
        self.pop_stack()

    def moins(self):
        self.stack[self.ip] *= -1

    def sous(self):
        self.stack[self.ip - 1] -= self.stack[self.ip]
        self.pop_stack()

    def add(self):
        self.stack[self.ip - 1] += self.stack[self.ip]
        self.pop_stack()

    def mult(self):
        self.stack[self.ip - 1] *= self.stack[self.ip]
        self.pop_stack()

    def div(self):
        self.stack[self.ip - 1] /= self.stack[self.ip]
        self.pop_stack()

    def egal(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] == self.stack[self.ip]
        self.pop_stack()

    def diff(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] != self.stack[self.ip]
        self.pop_stack()

    def inf(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] < self.stack[self.ip]
        self.pop_stack()

    def infeg(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] <= self.stack[self.ip]
        self.pop_stack()

    def sup(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] > self.stack[self.ip]
        self.pop_stack()

    def supeg(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] >= self.stack[self.ip]
        self.pop_stack()

    def et(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] and self.stack[self.ip]
        self.pop_stack()

    def ou(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] or self.stack[self.ip]
        self.pop_stack()

    def non(self):
        self.stack[self.ip] = not self.stack[self.ip]


    def tra(self, adresse: int):
        self.co = adresse

    def tze(self, adresse: int):
        if self.stack[self.ip] == 0:
            self.tra(adresse)
        else : 
            self.co -= 1 
        
        self.pop_stack()

    def erreur(self, exp : str):
        raise Exception(exp)

    def empilerTas(self, val : int):
        self.stack[self.ipTas]=val
        self.ipTas-=1

    def empilerIpTas(self):
        self.empilerAd(self.ip)
        self.stack[self.ipTas] = self.ip

    def empilerAdAt(self, v : int):
        '''Retrieving the dynamic address'''
        
        self.empiler(self.ipTas - v)

    def reserverBloc(self):
        '''Stacking the base block at the end of stack, but what's the base block size ? '''

        pass #TODO

    def retourConst(self):
        '''To do'''

        pass

    def retourFonct(self):
        '''To do'''

        pass

    def retourProc(self):
        '''To do'''

        pass

    def empilerParam(self):
        '''To do'''

        pass
    
    def traStat(self):
        '''To do '''

        pass

    def traConstr(self):
        '''To do'''

        pass

    def traVirt(self):
        '''To do'''

        pass


    def execute_instruction(self, instruction):
        '''Execute an instruction Nilnovi'''

        nom_instr = instruction[0]

        if hasattr(self, nom_instr):
            method = getattr(self, nom_instr)
            if len(instruction) > 1:
                method(*instruction[1:])
            else:
                method()
        else:
            raise ValueError(f"Unknown instruction: {nom_instr}")


def parse_nilnovi_object_line(line: str) -> list[str | int]:
    '''
    Parse a line of a nilnovi (object) line.

    Example :
    reserver(2) -> ['reserver', 2]
    '''

    ret = []
    line = line.strip('\n')

    if '()' in line or '(' not in line:
        return [line.strip('()')]
    
    ret.append(line[:line.index('(')])
    ret.append(int(line[line.index('(')+1:line.index(')')]))

    return ret


def run_vm(fn: str):
    '''
    Running the vm using a file.
    '''
    
    with open(fn, 'r') as f:
        instructions = f.read()
        vm = VM(instructions)

        vm.run(debug=True)

if __name__ == "__main__":
    from sys import argv
    run_vm(argv[1])
