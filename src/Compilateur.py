class Compilateur:
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

        if ligne[0] ==  "Keyword":
            if ligne[4] == "procedure":
                indice_begin = startIndex + 1
                profondeur = 0
                while profondeur != 0 or anaLexLinesSplit[indice_begin][0] != "Keyword" or anaLexLinesSplit[indice_begin][4] != "begin":
                    indice_begin += 1
                    if anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "procedure":
                        profondeur += 1
                    elif anaLexLinesSplit[indice_begin][0] == "Keyword" and anaLexLinesSplit[indice_begin][4] == "begin":
                        profondeur -= 1
                indice_end = endIndex
                while anaLexLinesSplit[indice_end][0] != "Keyword" or anaLexLinesSplit[indice_end][4] != "end":
                    indice_end -= 1
                self.outputFile.write("debutProg();\n")
                self.compile(anaLexLinesSplit, startIndex + 1, indice_begin - 1)
                self.compile(anaLexLinesSplit, indice_begin + 1, indice_end - 1)
                self.outputFile.write("finProg();\n")
        
        elif ligne[0] == "Integer":
            self.outputFile.write("empile(" , ligne[4], ")\n")
        else :
            print("Erreur de compilation")


        
    def main(self):
        """
        Fonction principale du compilateur
        """
        anaLexLinesSplit = self.anaLexLinesSplit(self.anaLexSplit())
        print(anaLexLinesSplit)
        self.compile()

        