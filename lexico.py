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

# Variable global para almacenar las palabras reconocidas con todos sus atributos
palabras_reconocidas = {}

# Construir el diccionario de palabras desde el JSON
palabras = {}
for categoria, items in lexico['palabras'].items():
    for palabra, datos in items.items():
        # Almacenar todos los datos de la palabra, no solo el tipo
        palabras[palabra] = datos

def t_PREPOSICION_A(t):
    r'a\b'
    palabras_reconocidas[t.value] = {
        'tipo': 'PREPOSICION_A',
        'palabra': t.value
    }
    return t

def t_ID(t):
    r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+'
    palabra_data = palabras.get(t.value)
    if palabra_data:
        t.type = palabra_data['tipo']
        # Almacenar todos los atributos de la palabra
        palabras_reconocidas[t.value] = {
            'tipo': palabra_data['tipo'],
            'palabra': t.value,
            'genero': palabra_data.get('genero', ''),
            'numero': palabra_data.get('numero', ''),
            'tiempo': palabra_data.get('tiempo', ''),
            'persona': palabra_data.get('persona', '')
        }
    else:
        t.type = 'ERROR'
        print(f"Palabra no reconocida: '{t.value}'")
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Función para obtener las palabras reconocidas
def obtener_palabras_reconocidas():
    return palabras_reconocidas.copy()

# Función para limpiar las palabras reconocidas (importante llamarla antes de cada nuevo análisis)
def limpiar_palabras_reconocidas():
    global palabras_reconocidas
    palabras_reconocidas = {}