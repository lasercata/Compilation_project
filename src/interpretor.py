class VM:
    def init(self):
        self.stack = []
        self.dictVariable = {}
        self.ptr=0

    def debutProg(self):
        pass
    def finProg(self):
        pass
    def reserver(self,n : int):
        self.stack += [None] * n
    def empiler(self,val : int):
        self.ptr += 1
        self.stack[self.ptr]=val
    def empilerAdresse(self,adresse : int):
        self.ptr += 1
        self.stack[self.ptr]=adresse
    def affectation(self,varName : str, varValue : int):
        self.dictVariable[varName]=varValue #self.stack[self.stack.index(None)-2]=self.stack[self.stack.index(null)-1]
    def valeurPile(self):
        self.stack[self.ptr] = self.stack[self.stack[self.ptr]]
    def get(self):
        self.stack[self.stack[self.ptr]] = input(">")
    def put(self): 
        # ça dépile aussi 
        print(self.stack.pop())
        self.ptr -= 1
    def moins(self):
        self.stack[-1]*=-1
    def sous(self):
        self.stack[-2] -= self.stack.pop()
        self.ptr -= 1
    def add(self):
        self.stack[-2] += self.stack.pop()
        self.ptr -= 1
    def mult(self):
        self.stack[-2] *= self.stack.pop()
        self.ptr -= 1
    def div(self):
        self.stack[-2] /= self.stack.pop()
        self.ptr -= 1
    def egal(self):
        self.stack[-2] = self.stack[-2] == self.stack.pop()
        self.ptr -= 1
    def diff(self):
        self.stack[-2] = self.stack[-2] != self.stack.pop()
        self.ptr -= 1
    def inf(self):
        self.stack[-2] = self.stack[-2] < self.stack.pop()
        self.ptr -= 1
    def infeg(self):
        self.stack[-2] = self.stack[-2] <= self.stack.pop()
        self.ptr -= 1
    def sup(self):
        self.stack[-2] = self.stack[-2] > self.stack.pop()
        self.ptr -= 1
    def supeg(self):
        self.stack[-2] = self.stack[-2] >= self.stack.pop()
        self.ptr -= 1
    def et(self):
        self.stack[-2] = self.stack[-2] and self.stack.pop()
        self.ptr -= 1
    def ou(self):
        self.stack[-2] = self.stack[-2] or self.stack.pop()
        self.ptr -= 1
    def non(self):
        self.stack[-1] = not self.stack[-1]
    def sauter(self, adresse : int):
        self.ptr = adresse
    def sauterSi(self, adresse : int):
        if self.stack.pop() == 0: 
            self.sauter(adresse)
    def erreur(self):
        raise Exception("Erreur d'exécution")




