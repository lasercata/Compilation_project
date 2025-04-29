import sys 

class VM: 
    '''Class defining the interpretor of the object code.'''

    def __init__(self, object_code: str, debug: bool = False):
        '''
        Constructor of the class.

        - object_code : the instructions (in object nilnovi) ;
        - debug       : boolean indicating if printing debug variables.
        '''

        self.instructions = object_code.split('\n')
        self.debug = debug

    def pop_stack(self) -> None | int | bool:
        '''
        Removes the top element of the stack.
        '''
    
        ret = self.stack[self.ip]
        del self.stack[self.ip]
        self.ip -= 1

        return ret

    def run(self):
        '''Runs the program.'''

        self.debutProg()
        self.co = 0
    
        last_line = len(self.instructions)

        try:
            while self.co < last_line:
                inst = self.instructions[self.co]
                parsed_instr = parse_nilnovi_object_line(inst)

                if self.debug:
                    print(f'Instruction : {parsed_instr}')
                    print(f'Stack       : {self.stack}')

                self.execute_instruction(parsed_instr)
                self.co += 1

        except Exception as e:
            print(f'Exception: {e}')
       

    def debutProg(self):
        '''Initialises the variables of the program.'''

        self.stack = []
        self.dictVariable = {}

        self.ip = -1 # The pointer to the summit of the stack. Increment when adding element.
        self.ipTas = -1 # The pointer to the summit of the heap (used as a stack). Decrement when adding element.

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
        self.stack[self.ip] = val

    def empilerAd(self, addr: int):
        self.empiler(self.stack[addr])

   # def _affectation(self, varName: str, varValue: int):
   #     self.dictVariable[varName] = varValue #self.stack[self.stack.index(None)-2]=self.stack[self.stack.index(null)-1]
    
    def affectation(self):
        self.stack[self.stack[self.ip - 1]]= self.stack[self.ip]
        self.pop_stack()
        self.pop_stack()

    def valeurPile(self):
        '''
        Replaces the summit of the stack by the elements designated by the current element on the summit of the stack.
        '''

        addr = self.stack[self.ip] # The old summit of the stack
        self.stack[self.ip] = self.stack[addr]

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
        '''
        Add to the summit of the stack the boolean value op1 != op2, where the stack is :

             ^
             |
            op2
            op1

        It remove op2 and op1 from the stack.
        '''

        op2 = self.pop_stack()
        op1 = self.pop_stack()

        self.empiler(op1 != op2)
        # print('here', op1 != op2, self.ip)

        # self.stack[self.ip - 1] = self.stack[self.ip - 1] != self.stack[self.ip]
        # self.pop_stack()

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


    def tra(self, addr: int):
        '''
        Jumps to the line `addr` in the instruction list (goto).

        The compiled code suppose that the lines are in range [|1 ; n|].
        In the internal representation, the instructions are in range [|0 ; n - 1|].
        This is the reason of the `-1`.

        - addr : the line to jump to.
        '''

        self.co = addr - 1

    def tze(self, addr: int):
        '''
        Checks the value at the summit of the stack, and if it is `False`, changes `self.co` to point to the instruction at line `addr`.

        - addr : the line to jump to in the object instructions, if the summit of the stack is `False`.
        '''

        if not self.pop_stack():
            self.tra(addr)

            if self.debug:
                print(f'tze: jumping at address {addr}')
        
    def erreur(self, exp : str):
        raise Exception(exp)

    def empilerTas(self, val : int):
        self.stack[self.ipTas] = val
        self.ipTas -= 1

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


def run_vm(fn: str, debug: bool = False):
    '''
    Running the vm using a file.
    '''
    
    with open(fn, 'r') as f:
        instructions = f.read()
        vm = VM(instructions, debug)

        vm.run()

if __name__ == "__main__":
    from sys import argv

    print(argv)

    if len(argv) == 3:
        debug = bool(int(argv[2]))
    else:
        debug = True

    run_vm(argv[1], debug)
