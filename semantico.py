from lexico import lexico
class AnalizadorSemantico:
    def __init__(self, lexico):
        self.errores = []
        self.genero = []
        self.lexico = lexico['palabras']
        self.oracion = {"pronombres": "nosotros", "determinantes": "la", "nombres_propios": "pizza"}
       

    def semanticValidation(self):
        errorType = []
        numero = []
        persona = []
        tiempo = []
        gender = []

        for key, value in self.oracion.items():
            datos = self.lexico[key][value]
            print(datos)

            if datos.get("numero"):
                numero.append(datos.get("numero"))

            if datos.get("persona"):
                persona.append(datos.get("persona"))

            if datos.get("tiempo"):
                tiempo.append(datos.get("tiempo"))

            if datos.get("tipo") != "VERBO":
                gender.append(datos.get("genero"))

        wordCounter = 0
        for word in numero:
            if wordCounter == 0:
                previousWord = word
                pass
            
            if previousWord != word:
                errorType.append(f"Number type mismatch: {previousWord}, {word}")
            
            previousWord = word
            wordCounter += 1
        
        wordCounter = 0
        for word in persona:
            if wordCounter == 0:
                previousWord = word
                pass
            
            if previousWord != word:
                errorType.append(f"Persona type mismatch: {previousWord}, {word}")
            
            previousWord = word
            wordCounter += 1

        wordCounter = 0
        for word in gender:
            if wordCounter == 0:
                previousWord = word
                pass
            
            if previousWord != word and word != None and previousWord != None:
                errorType.append(f"Gender type mismatch: {previousWord}, {word}")
            
            previousWord = word
            wordCounter += 1
        
        wordCounter = 0
        for word in tiempo:
            if wordCounter == 0:
                previousWord = word
                pass
            
            if previousWord != word:
                errorType.append(f"Tiempo type mismatch: {previousWord}, {word}")
            
            previousWord = word
            wordCounter += 1    
        
        if errorType:
            return errorType

    
            
                  

    
anlz = AnalizadorSemantico(lexico)
print(anlz.semanticValidation())
