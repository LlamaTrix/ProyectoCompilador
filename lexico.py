import json
import ply.lex as lex

try:
    with open('lexico.json', 'r', encoding='utf-8') as f:
        lexico = json.load(f)
    print("Diccionario cargado correctamente")
except Exception as e:
    print(f"Error al cargar lexico.json: {str(e)}")
    lexico = {'palabras': {}}  # Diccionario vacío como fallback

tokens = (
    'DETERMINANTE',
    'SUSTANTIVO',
    'VERBO',
    'ADJETIVO',
    'PRONOMBRE',
    'NOMBRE_PROPIO',
    'ADVERBIO',
    'PREPOSICION_A',
    'ERROR'
)

# Construir el diccionario de palabras desde el JSON
palabras = {}
for categoria, items in lexico['palabras'].items():
    for palabra, datos in items.items():
        palabras[palabra] = datos['tipo']

def t_PREPOSICION_A(t):
    r'a\b'
    return t

def t_ID(t):
    r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+'
    t.type = palabras.get(t.value, 'ERROR')
    if t.type == 'ERROR':
        print(f"Palabra no reconocida: '{t.value}'")
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()