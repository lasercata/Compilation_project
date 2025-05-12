class Compiler:
    
    # List of object code instructions
    compiled_possible_instructions = [
        "debutProg", "finProg", "reserver", "empiler", "empilerAdresse", "affectation",
        "valeurPile", "get", "put", "moins", "sous", "add", "mult", "div", "egal", "diff",
        "inf", "infegal", "sup", "supeg", "et", "ou", "non", "tra", "tze", "erreur",
        "empilerTas", "empilerIpTas", "empilerAdAt", "reserverBloc", "retourConstr",
        "retourFonct", "retourProc", "empilerParam", "traConstr", "traVirt"
    ]
    
    def __init__(self, fileName=None):
        #self.outputFile = open(fileName + "_compiled.txt", "w+")
        self.instructions = []
        
    ##########################################################
    #                   Simple instructions                  #
    ##########################################################
    
    def debutProg(self):
        self.instructions.append(["debutProg", []])
    
    def finProg(self):
        self.instructions.append(["finProg", []])
        
    def reserver(self, n : int):
        self.instructions.append(["reserver", [n]])
        
    def empiler(self, val : int):
        self.instructions.append(["empiler", [val]])
        
    def empilerAdresse(self, ad : int):
        self.instructions.append(["empilerAd", [ad]])
    
    def affectation(self):
        self.instructions.append(["affectation", []])

    def valeurPile(self):
        self.instructions.append(["valeurPile", []])
        
    def get(self):
        self.instructions.append(["get", []])
        
    def put(self):
        self.instructions.append(["put", []])
        
    def moins(self):
        self.instructions.append(["moins", []])
        
    def sous(self):
        self.instructions.append(["sous", []])
    
    def add(self):
        self.instructions.append(["add", []])
        
    def mult(self):
        self.instructions.append(["mult", []])
    
    def div(self):
        self.instructions.append(["div", []])
    
    def egal(self):
        self.instructions.append(["egal", []])
        
    def diff(self):
        self.instructions.append(["diff", []])
        
    def inf(self):
        self.instructions.append(["inf", []])
        
    def infegal(self):
        self.instructions.append(["infegal", []])
        
    def sup(self):
        self.instructions.append(["sup", []])
        
    def supeg(self):
        self.instructions.append(["supeg", []])
        
    def et(self):
        self.instructions.append(["et", []])
        
    def ou(self):
        self.instructions.append(["ou", []])
        
    def non(self):
        self.instructions.append(["non", []])
        
    def tra(self, ad : int):
        self.instructions.append(["tra", [ad]])
        
    def tze(self, ad : int):
        self.instructions.append(["tze", [ad]])
    
    def erreur(self):
        self.instructions.append(["erreur", []])
        
    def empilerTas(self, val : int):
        self.instructions.append(["empilerTas", [val]])
    
    def empilerIpTas(self):
        self.instructions.append(["empilerIpTas", []])
        
    def empilerAdAt(self, v : int):
        self.instructions.append(["empilerAdAt", [v]])
        
    def reserverBloc(self):
        self.instructions.append(["reserverBloc", []])
        
    def retourConstr(self):
        self.instructions.append(["retourConstr", []])
    
    def retourFonct(self):
        self.instructions.append(["retourFonct", []])
    
    def retourProc(self):
        self.instructions.append(["retourProc", []])
        
    def empilerParam(self, ad : int):
        self.instructions.append(["empilerParam", [ad]])
        
    def traConstr(self, ad : int, nbP : int):
        self.instructions.append(["traConstr", [ad, nbP]])
    
    def traVirt(self, i : int, nbP : int):
        self.instructions.append(["traVirt", [i, nbP]])

    

    ##########################################################
    #                     Compiler result                    #
    ##########################################################
    def instructions_to_string(self):
        string = ""
        for instruction in self.instructions:
            print(instruction)
            string += instruction[0] + "("
            for i in range(len(instruction[1])):
                string += str(instruction[1][i])
                if i != len(instruction[1]) - 1:
                    string += ", "
            string += ")\n"
        return string
    
    
            
        
    