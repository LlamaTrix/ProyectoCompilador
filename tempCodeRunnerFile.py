from flask import Flask, render_template, request, jsonify
import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph
import os
import random
import json

app = Flask(__name__)

# Al inicio de app.py, después de los imports
try:
    with open('lexico.json', 'r', encoding='utf-8') as f:
        lexico = json.load(f)
    print("Diccionario cargado correctamente")
except Exception as e:
    print(f"Error al cargar lexico.json: {str(e)}")
    lexico = {'palabras': {}}  # Diccionario vacío como fallback

# ----------------------------
# LEXER Y PARSER (actualizado)
# ----------------------------

tokens = (
    'DETERMINANTE',
    'SUSTANTIVO',
    'VERBO',
    'ADJETIVO',
    'PRONOMBRE',
    'NOMBRE_PROPIO',
    'ADVERBIO',
    'PREPOSICION_A',
    'ERROR'  # Añadido para manejar palabras desconocidas
)

# Lexer
def t_PREPOSICION_A(t):
    r'a\b'  # Solo la preposición 'a' como palabra completa
    return t

# Construir el diccionario de palabras desde el JSON
palabras = {}
for categoria, items in lexico['palabras'].items():
    for palabra, datos in items.items():
        palabras[palabra] = datos['tipo']

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

# Parser
def p_oracion(p):
    '''oracion : sujeto predicado'''
    p[0] = ('ORACION', p[1], p[2])

def p_sujeto(p):
    '''sujeto : sintagma_nominal'''
    p[0] = ('SUJETO', p[1])

def p_sintagma_nominal(p):
    '''
    sintagma_nominal : determinante sustantivo
                    | determinante sustantivo adjetivo
                    | pronombre
                    | nombre_propio
    '''
    if len(p) == 3:
        p[0] = ('SN', p[1], p[2])
    elif len(p) == 4:
        p[0] = ('SN', p[1], p[2], p[3])
    else:
        p[0] = ('SN', p[1])

def p_predicado(p):
    '''
    predicado : verbo
              | verbo complemento_directo
              | verbo complemento_directo complemento_indirecto
              | verbo complemento_directo adverbio
              | verbo complemento_indirecto
              | verbo adverbio
    '''
    p[0] = ('PREDICADO', *p[1:])

def p_complemento_directo(p):
    '''complemento_directo : sintagma_nominal'''
    p[0] = ('CD', p[1])

def p_complemento_indirecto(p):
    '''complemento_indirecto : PREPOSICION_A sintagma_nominal'''
    p[0] = ('CI', p[2])

# Terminales
def p_determinante(p):
    '''determinante : DETERMINANTE'''
    p[0] = ('DET', p[1])

def p_sustantivo(p):
    '''sustantivo : SUSTANTIVO'''
    p[0] = ('SUST', p[1])

def p_verbo(p):
    '''verbo : VERBO'''
    p[0] = ('VERBO', p[1])

def p_adjetivo(p):
    '''adjetivo : ADJETIVO'''
    p[0] = ('ADJ', p[1])

def p_pronombre(p):
    '''pronombre : PRONOMBRE'''
    p[0] = ('PRON', p[1])

def p_nombre_propio(p):
    '''nombre_propio : NOMBRE_PROPIO'''
    p[0] = ('NOMBRE', p[1])

def p_adverbio(p):
    '''adverbio : ADVERBIO'''
    p[0] = ('ADV', p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en: '{p.value}'")
    else:
        print("Error de sintaxis: fin inesperado de entrada")

parser = yacc.yacc()

# ----------------------------
# VISUALIZACIÓN DEL ÁRBOL
# ----------------------------

def generar_imagen_arbol(arbol):
    dot = Digraph(comment='Árbol Sintáctico')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica')
    
    def agregar_nodos(padre, nodo):
        if isinstance(nodo, tuple):
            nombre = str(id(nodo)) + nodo[0]
            dot.node(nombre, nodo[0])
            if padre:
                dot.edge(padre, nombre)
            for hijo in nodo[1:]:
                agregar_nodos(nombre, hijo)
        else:
            nombre_hoja = str(id(nodo)) + str(nodo)
            dot.node(nombre_hoja, nodo)
            if padre:
                dot.edge(padre, nombre_hoja)
    
    agregar_nodos(None, arbol)
    
    # Guardar imagen temporal
    if not os.path.exists('static'):
        os.makedirs('static')
    ruta_imagen = 'static/arbol.png'
    dot.render('static/arbol', format='png', cleanup=True)
    return ruta_imagen

# ----------------------------
# RUTAS FLASK
# ----------------------------

def generar_ejemplos():
    ejemplos = []
    lex = lexico['palabras']  # Corregido: era 'palabras' no 'palabras'
    
    # Ejemplo 1: Determinante + Sustantivo + Verbo
    det = random.choice(list(lex['determinantes'].keys()))
    sust = random.choice(list(lex['sustantivos'].keys()))
    verb = random.choice(list(lex['verbos'].keys()))
    ejemplos.append(f"{det} {sust} {verb}")
    
    # Ejemplo 2: Nombre propio + Verbo + Adverbio
    nom = random.choice(list(lex['nombres_propios'].keys()))
    verb = random.choice(list(lex['verbos'].keys()))
    adv = random.choice(list(lex['adverbios'].keys()))
    ejemplos.append(f"{nom} {verb} {adv}")
    
    # Ejemplo 3: Determinante + Sustantivo + Adjetivo + Verbo
    det = random.choice(list(lex['determinantes'].keys()))
    sust = random.choice(list(lex['sustantivos'].keys()))
    adj = random.choice(list(lex['adjetivos'].keys()))
    verb = random.choice(list(lex['verbos'].keys()))
    ejemplos.append(f"{det} {sust} {adj} {verb}")
    
    return ejemplos

@app.route('/', methods=['GET', 'POST'])
def index():
    significado = None
    arbol_imagen = None
    error = None
    frase = ""
    
    return render_template('index.html', 
                         significado=significado,
                         arbol_imagen=arbol_imagen,
                         error=error,
                         frase_ejemplo=frase)

@app.route('/analizar', methods=['POST'])
def analizar():
    frase = request.form.get('frase', '')
    significado = None
    arbol_imagen = None
    error = None

    try:
        resultado = parser.parse(frase, lexer=lexer)
        significado = "Oración válida según la gramática del español"

        # Generar imagen y guardar como archivo accesible
        arbol_imagen = generar_imagen_arbol(resultado)  # Esto ya guarda en static/arbol.png
        arbol_imagen = '/' + arbol_imagen  # Para que sea usable desde HTML

    except Exception as e:
        error = f"Error al analizar: {str(e)}"

    return jsonify({
        'significado': significado,
        'arbol_imagen': arbol_imagen,
        'error': error
    })


@app.route('/get_diccionario')
def get_diccionario():
    try:
        lex = lexico['palabras']
        return jsonify({
            'determinantes': list(lex.get('determinantes', {}).keys()),
            'sustantivos': list(lex.get('sustantivos', {}).keys()),
            'verbos': list(lex.get('verbos', {}).keys()),
            'adjetivos': list(lex.get('adjetivos', {}).keys()),
            'adverbios': list(lex.get('adverbios', {}).keys()),
            'pronombres': list(lex.get('pronombres', {}).keys()),
            'nombres_propios': list(lex.get('nombres_propios', {}).keys())
        })
    except Exception as e:
        print(f"Error al cargar diccionario: {str(e)}")
        return jsonify({
            'determinantes': [],
            'sustantivos': [],
            'verbos': [],
            'adjetivos': [],
            'adverbios': [],
            'pronombres': [],
            'nombres_propios': []
        })

# Añade esta función a tu app.py
@app.route('/generar_ejemplo_inteligente')
def generar_ejemplo_inteligente():
    def construir_frase():
        lex = lexico['palabras']
        estructuras = [
            lambda: f"{random.choice(list(lex['determinantes'].keys()))} {random.choice(list(lex['sustantivos'].keys()))} {random.choice(list(lex['verbos'].keys()))}",
            lambda: f"{random.choice(list(lex['nombres_propios'].keys()))} {random.choice(list(lex['verbos'].keys()))} {random.choice(list(lex['adverbios'].keys()))}",
            lambda: f"{random.choice(list(lex['pronombres'].keys()))} {random.choice(list(lex['verbos'].keys()))} {random.choice(list(lex['determinantes'].keys()))} {random.choice(list(lex['sustantivos'].keys()))}",
            lambda: f"{random.choice(list(lex['determinantes'].keys()))} {random.choice(list(lex['sustantivos'].keys()))} {random.choice(list(lex['verbos'].keys()))} a {random.choice(list(lex['determinantes'].keys()))} {random.choice(list(lex['sustantivos'].keys()))}"
        ]
        return random.choice(estructuras)()
    
    return jsonify({'frase': construir_frase()})

@app.route('/get_word_info')
def get_word_info():
    word = request.args.get('word')
    lex = lexico['palabras']
    
    # Buscar la palabra en todas las categorías
    for category, words in lex.items():
        if word in words:
            word_data = words[word]
            return jsonify({
                'palabra': word,
                'tipo': word_data['tipo'].lower(),
                'genero': word_data.get('genero', ''),
                'numero': word_data.get('numero', ''),
                'tiempo': word_data.get('tiempo', ''),
                'info': f"Información detallada de '{word}' como {word_data['tipo'].lower()}"
            })
    
    # Si no se encuentra la palabra
    return jsonify({
        'palabra': word,
        'tipo': 'desconocido',
        'info': 'Esta palabra no está en nuestro diccionario'
    }), 404

if __name__ == '__main__':
    app.run(debug=True)