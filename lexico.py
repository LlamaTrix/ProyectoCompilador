import json
import ply.lex as lex

class Lexico:
    def __init__(self):
        self.palabras = self.cargar_diccionario()
        self.tokens = (
            'DETERMINANTE', 'SUSTANTIVO', 'VERBO', 'ADJETIVO', 'CONJUNCION',
            'PRONOMBRE', 'NOMBRE_PROPIO', 'ADVERBIO', 'PREPOSICION', 'NEGACION', 'NUMERO'
        )
        self.lexer = lex.lex(module=self)
        self.errores = []

    def cargar_diccionario(self):
        try:
            with open('lexico.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                plano = {}
                for categoria in data.get("palabras", {}):
                    for palabra, atributos in data["palabras"][categoria].items():
                        atributos['tipo'] = categoria.upper()
                        plano[palabra.lower()] = atributos
                return plano
        except Exception as e:
            print(f"Error al cargar lexico.json: {str(e)}")
            return {}

    def obtener_diccionario_clasificado(self):
        try:
            with open('lexico.json', 'r', encoding='utf-8') as f:
                return json.load(f).get("palabras", {})
        except Exception as e:
            print(f"Error al cargar lexico.json: {str(e)}")
            return {}

    def t_NEGACION(self, t):
        r'\bno\b'
        t.value = t.value.lower()
        return t
    
    def t_NUMERO(self, t):
        r'\d+'
        return t

    def t_ID(self, t):
        r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+'
        t.value = t.value.lower()
        palabra_data = self.palabras.get(t.value)
        if palabra_data:
            t.type = palabra_data['tipo']
        else:
            t.type = 'ERROR'
            self.errores.append(f"Palabra no reconocida: '{t.value}'")
        return t

    t_ignore = ' \t\n'

    def t_error(self, t):
        self.errores.append(f"Carácter ilegal: '{t.value[0]}'")
        t.lexer.skip(1)

    def analizar(self, texto):
        self.errores = []  # Reiniciar errores
        self.lexer.input(texto)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return {
            'tokens': tokens,
            'error_lexico': self.errores
        }
