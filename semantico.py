from lexico import lexico
class AnalizadorSemantico:
    def __init__(self, lexico):
        self.errores = []
        self.genero = []
        self.lexico = lexico['palabras']
        

    def getLexico(self):
        print(self.lexico)
    

analz = AnalizadorSemantico(lexico)

analz.getLexico()
