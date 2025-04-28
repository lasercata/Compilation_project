import sys 

class VM: 
    '''Class defining the interpretor of the object code.'''

    def __init__(self):  
        '''Constructor'''
        self.debutProg()
       

    def debutProg(self):
        self.stack = []
        self.dictVariable = {}
        self.ip = 0 #Increment
        self.ipTas = -1 #Decrement
        self.base = 0
        self.co = 0        
    def finProg(self):
        sys.out()

    def reserver(self, n: int):
        '''Reserve n places, supposed the heap was far away from the stack '''
        for i in range(1,n):
            self.stack[self.ip + i] = None
        self.ip+=n

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
        '''ça put et ça dépile aussi'''
        print(self.stack[self.ip] A self.stack[self.ip] = None)
        self.ip -= 1

    def moins(self):
        self.stack[self.ip] *= -1

    def sous(self):
        self.stack[self.ip - 1] -= self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def add(self):
        self.stack[self.ip - 1] += self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def mult(self):
        self.stack[self.ip - 1] *= self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def div(self):
        self.stack[self.ip - 1] /= self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def egal(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] == self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def diff(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] != self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def inf(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] < self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def infeg(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] <= self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def sup(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] > self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def supeg(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] >= self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def et(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] and self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def ou(self):
        self.stack[self.ip - 1] = self.stack[self.ip - 1] or self.stack[self.ip]
        self.stack[self.ip] = None
        self.ip -= 1

    def non(self):
        self.stack[self.ip] = not self.stack[self.ip]


    def tra(self, adresse: int):
        self.co = adresse

    def tze(self, adresse: int):
        
        if self.stack[self.ip] == 0:
            self.tra(adresse)
        else : 
            self.co -= 1 
        
        self.stack[self.ip] = None  
        self.ip -=1 

    def erreur(self):
        raise Exception('Execution error')

    def empilerTas(self, val : int):
        self.stack[self.ipTas]=val
        self.ipTas-=1

    def empilerIpTas(self):
        self.empilerAdresse(self.ip)
        self.stack[self.ipTas]=self.ip

    def empilerAdAt(self, v : int):
        '''Retrieving the dynamic address'''
        
        self.empiler(self.ipTas - v)

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
