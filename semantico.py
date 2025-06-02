import json
from lexico import lexico

try:
    with open('semantico.json', 'r', encoding='utf-8') as f:
        semantico = json.load(f)
    print("Diccionario cargado correctamente")
except Exception as e:
    print(f"Error al cargar lexico.json: {str(e)}")
    semantico = {'phrases': {}}  # Diccionario vacío como fallback



class AnalizadorSemantico:
    def __init__(self, lexico, semantico, oracion, oracionTokens):
        self.errores = []
        self.genero = []
        self.lexico = lexico['palabras']
        self.semantico = semantico['phrases']
        self.oracionTokens = oracionTokens
        self.oracion = oracion
       

    def semanticValidation(self):
        errorType = []
        numero = []
        persona = []
        tiempo = []
        gender = []

        for key, value in self.oracionTokens.items():
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

    def femaleTranslation(self):
        try:
            with open('semantico.json', 'r', encoding='utf-8') as f:
                semantico = json.load(f)
            print("Diccionario cargado correctamente")
        except Exception as e:
            print(f"Error al cargar semantico.json: {str(e)}")
            semantico = {'phrases': {}}  # Diccionario vacío como fallback

        for key, values in self.semantico.items():
            if self.oracion == key:
                val = values.get("significado")
                print(f"La frase: {self.oracion} realmente significa: {val}")
        


     
anlz = AnalizadorSemantico(lexico, semantico, oracion, oracionTokens)