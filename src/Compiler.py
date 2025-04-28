class Compiler:
    def __init__(self, anaLexResult, fileName):
        self.anaLexResult = anaLexResult
        self.outputFile = open(fileName + "_compiled.txt", "w+")
    
    def anaLexSplit(self):
        """
        Fonction qui sépare les lignes du résultat de l'analyse lexicale
        """
        anaLexLines = self.anaLexResult.split("\n")
        return anaLexLines

    def anaLexLinesSplit(self, analexLines):
        """
        Fonction qui sépare les mots dans les lignes de chaque case du tableau
        """
        return [line.split() for line in analexLines]
    
    def compile(self, anaLexLinesSplit, startIndex, endIndex):
        """
        Fonction qui compile le code
        """

        #self.outputFile.write("")
        #self.outputFile.close()
        
        ligne = anaLexLinesSplit[startIndex]

        if (endIndex >= startIndex) :
            if ligne[0] ==  "Keyword":
                # on repère les procédures
                if ligne[4] == "procedure":
                    # On cherche la ligne du begin
                    indice_begin = startIndex + 1
                    profondeur = 0
                    while profondeur != 0 or anaLexLinesSplit[indice_begin][0] != "Keyword" or anaLexLinesSplit[indice_begin][4] != "begin":
                        if anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "procedure":
                            profondeur += 1
                        elif anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "begin":
                            profondeur -= 1
                        indice_begin += 1
                    # On cherche la ligne du end
                    indice_end = startIndex + 1
                    profondeur = 0
                    while profondeur != 0 or anaLexLinesSplit[indice_end][0] != "Keyword" or anaLexLinesSplit[indice_end][4] != "end":
                        if anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "procedure":
                            profondeur += 1
                        elif anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "end":
                            profondeur -= 1
                        indice_end += 1
                        
                    self.outputFile.write("debutProg();\n")
                    self.compile(anaLexLinesSplit, startIndex + 1, indice_begin - 1)
                    self.compile(anaLexLinesSplit, indice_begin + 1, indice_end - 1)
                    self.outputFile.write("finProg();\n")
                
                elif ligne[4] == "put":
                    indice_parenthese_ouvrante = startIndex + 1
                    indice_parenthese_fermante = indice_parenthese_ouvrante + 1
                    profondeur = 0
                    while profondeur != 0 or anaLexLinesSplit[indice_parenthese_fermante][0] != "Keyword" or anaLexLinesSplit[indice_parenthese_fermante][4] != ")":
                        if anaLexLinesSplit[indice_parenthese_fermante][0] == "Keyword" and anaLexLinesSplit[indice_parenthese_fermante][4] == "(":
                            profondeur += 1
                        elif anaLexLinesSplit[indice_parenthese_fermante][0] == "Keyword" and anaLexLinesSplit[indice_parenthese_fermante][4] == ")":
                            profondeur -= 1
                        indice_parenthese_fermante += 1
                    self.compile(anaLexLinesSplit, indice_parenthese_ouvrante + 1, indice_parenthese_fermante - 1)
                    self.outputFile.write("put()\n")
                
                elif ligne[4] == "true":
                    self.outputFile.write("empiler(1)\n")
                    self.compile(anaLexLinesSplit, startIndex + 1, endIndex)
                elif ligne[4] == "false":
                    self.outputFile.write("empiler(0)\n")
                    self.compile(anaLexLinesSplit, startIndex + 1, endIndex)
                    
                elif ligne[4] in ["boolean","integer"]:
                    print("CA DOIT RESERVER")
                    # On compte le nombre de variable à déclarer
                    nb_variables = 0
                    indice_dans_ligne = startIndex - 1
                    while anaLexLinesSplit[indice_dans_ligne][1] == ligne[1]:
                        if anaLexLinesSplit[indice_dans_ligne][0] == "Identifier":
                            nb_variables += 1
                        indice_dans_ligne -= 1
                    self.outputFile.write("reserver(" + nb_variables +")")


            elif ligne[0] == "Integer":
                # Compilation d'une valeur entière
                print("Compilation d'une valeur entière")
                self.outputFile.write("empile(" + ligne[4] + ")\n")
                self.compile(anaLexLinesSplit, startIndex + 1, endIndex)
                
            elif (ligne[0] == "Character" and ligne[4] in ["-", "+", "*", "/"]) or (ligne[0] == "Symbol" and ligne[4] in ["=", "<", ">", "<=", ">=", "/="]) or (ligne[0] == "Keyword" and ligne[4] in ["and", "or"]):
                    # Compilation des opérations binaires
                    print("Compilation d'une opération")
                    leftEnd = startIndex - 1
                    rightStart = startIndex + 1
                    leftStart = leftEnd - 1
                    rightEnd = rightStart + 1
                    while anaLexLinesSplit[leftStart][4] != ";":
                        leftStart -= 1
                    while anaLexLinesSplit[rightEnd][4] != ";":
                        rightEnd += 1
                    self.compile(anaLexLinesSplit, leftStart, leftEnd)
                    self.compile(anaLexLinesSplit, rightStart, rightEnd)
                    if ligne[4] == "-":
                        self.outputFile.write("sous();")
                    elif ligne[4] == "+":
                        self.outputFile.write("add();")
                    elif ligne[4] == "*":
                        self.outputFile.write("mult();")
                    elif ligne[4] == "/":
                        self.outputFile.write("div();")
                    elif ligne[4] == "=":
                        self.outputFile.write("egal();")
                    elif ligne[4] == "<":
                        self.outputFile.write("inf();")
                    elif ligne[4] == ">":
                        self.outputFile.write("sup();")
                    elif ligne[4] == "<=":
                        self.outputFile.write("infeg();")
                    elif ligne[4] == ">=":
                        self.outputFile.write("supeg();")
                    elif ligne[4] == "/=":
                        self.outputFile.write("diff();")
                    elif ligne[4] == "and":
                        self.outputFile.write("et();")
                    elif ligne[4] == "or":
                        self.outputFile.write("ou();")
                        
            else :
                self.compile(anaLexLinesSplit, startIndex + 1, endIndex)
        
        

        
    def main(self):
        """
        Fonction principale du compilateur
        """
        anaLexLinesSplit = self.anaLexLinesSplit(self.anaLexSplit())
        print(anaLexLinesSplit)
        self.compile(anaLexLinesSplit, 0, len(anaLexLinesSplit) - 1)
        self.outputFile.close()
        
