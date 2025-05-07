#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''File implementing the interpretor of the object code.'''

##-Imports
# import sys 
from typing import Any

##-Interpretor
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

    # ====== Init
    def debutProg(self):
        '''Initialises the variables of the program.'''

        # self.stack = []
        self.stack = Stack()
        self.heap = Stack()
        self.dictVariable = {}

        # self.ip = -1 # The pointer to the summit of the stack. Increment when adding element.
        # self.ipTas = -1 # The pointer to the summit of the heap (used as a stack). Decrement when adding element.

        self.base = 0

    def finProg(self):
        raise Exception('Program ended')

    # ====== Stack operations
    def reserver(self, n: int):
        '''Reserve n places, supposed the heap was far away from the stack '''

        for _ in range(0, n):
            self.stack.push(None)

    def empiler(self, val: int):
        '''Pushes `val` to the summit of the stack.'''

        self.stack.push(val)

    def empilerAd(self, addr: int):
        '''
        Pushes the element at address `self.base + addr` to the summit of the stack.
        '''

        self.empiler(self.stack.get_value_at(addr + self.base))

    def affectation(self):
        '''
        Places the value at the summit at the address designated by the value under the summit.
        Pops the two top elements from the stack.
        '''

        value = self.stack.pop()
        addr = self.stack.pop()

        self.stack.set_value_at(addr, value)

    def valeurPile(self):
        '''
        Replaces the summit of the stack by the elements designated by the current element on the summit of the stack.
        '''

        addr = self.stack.pop()
        value = self.stack.get_value_at(addr)
        self.stack.push(value)

    # ====== IO operations
    def get(self):
        '''
        Reads input from user, and write it to the address designated by the summit of the stack.
        Pops the summit.
        '''

        addr = self.stack.pop()
        self.stack.set_value_at(addr, input('>'))

    def put(self):
        '''Prints the summit of the stack, after pop it.'''

        print(self.stack.pop())

    # ====== Arithmetic operations
    def moins(self):
        '''Unary operation, calculates the opposite of the summit of the stack and replace it.'''

        value = self.stack.pop()
        self.stack.push(-value)

    def sous(self):
        '''
        Substraction.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 - op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 - op2)

    def add(self):
        '''
        Addition.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 + op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 + op2)

    def mult(self):
        '''
        Multiplication.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 * op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 * op2)

    def div(self):
        '''
        Division.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 / op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 / op2)

    # ====== Boolean operations
    def egal(self):
        '''
        Equality test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 == op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 == op2)

    def diff(self):
        '''
        Difference test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 != op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 != op2)

    def inf(self):
        '''
        Strict inferiority test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 < op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 < op2)

    def infeg(self):
        '''
        Inferiority test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 <= op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 <= op2)

    def sup(self):
        '''
        Strict superiority test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 > op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 > op2)

    def supeg(self):
        '''
        Superiority test.
        Pop `op2` and `op1` from the summit of the stack, and push `op1 >= op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 >= op2)

    def et(self):
        '''
        AND boolean operation
        Pop `op2` and `op1` from the summit of the stack, and push `op1 AND op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 and op2)

    def ou(self):
        '''
        OR boolean operation
        Pop `op2` and `op1` from the summit of the stack, and push `op1 OR op2`.
        '''

        op2 = self.stack.pop()
        op1 = self.stack.pop()

        self.stack.push(op1 or op2)

    def non(self):
        '''
        NOT boolean operation
        Pop `op1` from the summit of the stack, and push `NOT op1`.
        '''

        op1 = self.stack.pop()

        self.stack.push(not op1)


    # ====== Goto operations
    def tra(self, addr: int):
        '''
        Jumps to the line `addr` in the instruction list (goto).

        The compiled code suppose that the lines are in range [|1 ; n|].
        In the internal representation, the instructions are in range [|0 ; n - 1|].
        So we need to use `addr - 1`.
        But the `self.co` is going to be incremented in the `run` method. So `-1` again.
        This is the reason of the `-2`.

        - addr : the line to jump to.
        '''

        self.co = addr - 2

    def tze(self, addr: int):
        '''
        Checks the value at the summit of the stack, and if it is `False`, changes `self.co` to point to the instruction at line `addr`.

        - addr : the line to jump to in the object instructions, if the summit of the stack is `False`.
        '''

        if not self.stack.pop():
            self.tra(addr)

            if self.debug:
                print(f'tze: jumping at address {addr}')

    # ====== Error
    def erreur(self, exp : str):
        raise Exception(exp)

    # ====== Heap operations
    def empilerTas(self, val : int):
        '''Pushes `val` to the heap.'''

        self.heap.push(val)

    def empilerIpTas(self):
        '''Pushes to the stack, the current address of the summit of the heap.'''

        heap_summit_addr = self.heap.ip # ipTas
        self.stack.push(heap_summit_addr)

    def empilerAdAt(self, v : int):
        '''
        Pushes to the stack, the address of the attribute #`v` in the stack.

        The start of the object in the heap is found at address `self.base - 1` in the stack.
        So the address to push to the stack is `heap[self.base - 1] + v`.
        '''
        
        obj_start_addr = self.stack.get_value_at(self.base - 1)
        self.stack.push(obj_start_addr + v)

    # ====== Operations
    def reserverBloc(self):
        '''Stacking the base block at the end of stack'''

        self.stack.push(self.base)
        self.stack.push(self.stack.get_value_at(self.base + 1))

    def retourConstr(self):
        '''
        Make sure the instance of the object delivers a reference by the top of the stack.
        '''
        
        ar = self.stack.get_value_at(self.base + 1)
        newbase = self.stack.get_value_at(self.stack.get_value_at(self.base))

        while(self.stack.ip >= self.base):
            self.stack.pop()

        self.base = newbase
        self.co = ar

    def retourFonct(self):
        '''Return of a function. Ensures that the summit of the stack is the result of the call.'''

        ar = self.stack.get_value_at(self.base + 1)
        value = self.stack.summit()
        newbase = self.stack.get_value_at(self.stack.get_value_at(self.base))

        while(self.stack.ip >= self.base):
            self.stack.pop()

        # self.stack[self.stack.ip]=value
        self.stack.set_value_at(self.stack.ip, value)
        self.base = newbase
        self.co = ar


    def retourProc(self):
        '''Return of a Procedure.'''

        ar = self.stack.get_value_at(self.base + 1)
        newbase = self.stack.get_value_at(self.stack.get_value_at(self.base))

        while(self.stack.ip >= self.base):
            self.stack.pop()

        self.stack.pop() #pop one more time because there isn't return value
        self.base = newbase
        self.co = ar


    def empilerParam(self, ad: int):
        '''handle effective parameters'''

        self.stack.push(self.stack.get_value_at(self.base + 2 + ad))
    
    def traConstr(self, ad: int, nbP: int):
        """_summary_

        Args:
            ad (int): starting address of the constructor.
            nbP (int): number of parameters of the constructor.
        """

        prefixe = self.stack.ip - nbP - 2  # watch out for the index offset !!!
        t_addr = self.stack.get_value_at(prefixe)
        t = self.heap.get_value_at(t_addr)

        # self.stack[prefixe + 2] = self.co
        self.stack.set_value_at(prefixe + 2, self.co - 1)
        self.co = ad
        self.base = prefixe + 1

        self.heap.push(t_addr)
        self.stack.set_value_at(prefixe, self.heap.ip)
        for _ in range(t):
            self.heap.push(None) #TODO: is it really None, or we put a value here ?

    def traStat(self):
        '''To do '''

        pass

    def traVirt(self):
        '''To do'''

        pass


    # ====== Execution
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
                    print(f'Stack       : {self.stack}')
                    print(f'Heap        : {self.heap}')
                    print(f'Instr ptr   : {self.co}')
                    print(f'Instruction : {parsed_instr}')
                    print()

                self.execute_instruction(parsed_instr)
                self.co += 1

        except Exception as e:
            if str(e) == 'Program ended':
                if self.debug:
                    print('Program finished.')

                return

            print(f'Exception: {e}')
       

##-Stack
class Stack:
    '''Defines a stack'''

    def __init__(self):
        '''Initiates the stack'''

        self.stack = [] # The stack structure
        self.ip = -1 # a pointer to the summit of the stack (last element of the list self.stack).

    def push(self, v: Any) -> None:
        '''
        Pushes the element `v` to the stack.

        - v : the element to push.
        '''
    
        self.stack.append(v)
        self.ip += 1

    def pop(self) -> Any:
        '''
        Removes the summit of the stack and return it.

        Raises a ValueError if the stack is empty.
        '''
    
        if self.ip == -1:
            raise ValueError('Cannot pop an empty stack !')
        
        ret = self.stack[self.ip]
        del self.stack[self.ip]
        self.ip -= 1

        return ret

    def summit(self) -> Any:
        '''
        Returns the element at the summit of the stack.

        If the stack is empty, raises a ValueError.
        '''
    
        if self.ip == -1:
            raise ValueError('Cannot get the summit of an empty stack !')
    
        return self.stack[self.ip]

    def get_value_at(self, addr: int) -> Any:
        '''
        Returns the value at the address `addr`.
        The addresses are in `[|0 ; ip|]`, where `ip` is the address of the summit of the stack :

            ^
            |
            ip
            .
            .
            .
            1
            0

        - addr : the address of the element to retreive.

        If `addr` is not in the range, raises a ValueError.
        '''

        if addr < 0 or self.ip < addr:
            raise ValueError(f'Stack: impossible to get value at address {addr}: out of bounds')
    
        return self.stack[addr]

    def set_value_at(self, addr: int, v: Any):
        '''
        Sets the value at `addr` to `v`.
        Raises a ValueError if `addr` is out of bounds.

        - v    : the value to set ;
        - addr : the address. Should be in the range described in `get_value_at`.
        '''

        if addr < 0 or self.ip < addr:
            raise ValueError(f'Stack: impossible to set value at address {addr}: out of bounds')

        self.stack[addr] = v

    def __repr__(self) -> str:
        '''Returns the representation of the stack.'''
    
        return str(self.stack) #TODO: make a better representation ?

        


##-Functions
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


def run_vm_from_file(fn: str, debug: bool = False):
    '''
    Running the vm using a file.
    '''
    
    with open(fn, 'r') as f:
        instructions = f.read()
        vm = VM(instructions, debug)

        vm.run()


##-Testing
if __name__ == "__main__":
    from sys import argv

    if len(argv) == 3:
        debug = bool(int(argv[2]))
    else:
        debug = True

    run_vm_from_file(argv[1], debug)
