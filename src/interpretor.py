class VM: 
    '''Class defining the interpretor of the object code.'''

    def __init__(self):  
        '''Constructor'''

        self.stack = []
        self.dictVariable = {}
        self.ip = 0 #Increment
        self.ipHeap = -1 #Decrement
        self.base = 0

    def debutProg(self):
        pass

    def finProg(self):
        pass

    def reserver(self, n: int):
        self.stack += [None] * n

    def empiler(self, val: int):
        self.ip += 1
        self.stack[self.ip]=val

    def empilerAdresse(self, adresse: int):
        self.ip += 1
        self.stack[self.ip] = adresse

    def affectation(self, varName: str, varValue: int):
        self.dictVariable[varName] = varValue #self.stack[self.stack.index(None)-2]=self.stack[self.stack.index(null)-1]

    def valeurPile(self):
        self.stack[self.ip] = self.stack[self.stack[self.ip]]

    def get(self):
        self.stack[self.stack[self.ip]] = input(">")

    def put(self):
        # ça dépile aussi
        print(self.stack.pop())
        self.ip -= 1

    def moins(self):
        self.stack[-1] *= -1

    def sous(self):
        self.stack[-2] -= self.stack.pop()
        self.ip -= 1

    def add(self):
        self.stack[-2] += self.stack.pop()
        self.ip -= 1

    def mult(self):
        self.stack[-2] *= self.stack.pop()
        self.ip -= 1

    def div(self):
        self.stack[-2] /= self.stack.pop()
        self.ip -= 1

    def egal(self):
        self.stack[-2] = self.stack[-2] == self.stack.pop()
        self.ip -= 1

    def diff(self):
        self.stack[-2] = self.stack[-2] != self.stack.pop()
        self.ip -= 1

    def inf(self):
        self.stack[-2] = self.stack[-2] < self.stack.pop()
        self.ip -= 1

    def infeg(self):
        self.stack[-2] = self.stack[-2] <= self.stack.pop()
        self.ip -= 1

    def sup(self):
        self.stack[-2] = self.stack[-2] > self.stack.pop()
        self.ip -= 1

    def supeg(self):
        self.stack[-2] = self.stack[-2] >= self.stack.pop()
        self.ip -= 1

    def et(self):
        self.stack[-2] = self.stack[-2] and self.stack.pop()
        self.ip -= 1

    def ou(self):
        self.stack[-2] = self.stack[-2] or self.stack.pop()
        self.ip -= 1

    def non(self):
        self.stack[-1] = not self.stack[-1]

    def sauter(self, adresse: int):
        self.ip = adresse

    def sauterSi(self, adresse: int):
        if self.stack.pop() == 0: 
            self.sauter(adresse)

    def erreur(self):
        raise Exception('Execution error')

    def empilerTas(self, val : int):
        self.stack[self.ipHeap]=val
        self.ipHeap-=1

    def empilerIpTas(self):
        self.empilerAdresse(self.ip)
        self.stack[self.ipHeap]=self.ip

    def empilerAdAt(self, v : int):
        '''Retrieving the dynamic address'''
        
        self.empiler(self.ipHeap - v)

    def reserverBloc(self):
        '''Stacking the base bloc at the end of stack, what's the base block size ? '''

        pass

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
    
    def traConstr(self):
        '''To do'''

        pass

    def traVirt(self):
        '''To do'''

        pass
