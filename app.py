
from flask import Flask, render_template, request, jsonify
from lexico import lexico, lexer
from sintactico import parser
from semantico import AnalizadorSemantico, generar_imagen_arbol
import random
import json
app = Flask(__name__)

def generar_ejemplos():
    ejemplos = []
    lex = lexico['palabras']
    
    det = random.choice(list(lex['determinantes'].keys()))
    sust = random.choice(list(lex['sustantivos'].keys()))
    verb = random.choice(list(lex['verbos'].keys()))
    ejemplos.append(f"{det} {sust} {verb}")
    
    nom = random.choice(list(lex['nombres_propios'].keys()))
    verb = random.choice(list(lex['verbos'].keys()))
    adv = random.choice(list(lex['adverbios'].keys()))
    ejemplos.append(f"{nom} {verb} {adv}")
    
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
    errores_semanticos = []

    try:
        resultado = parser.parse(frase, lexer=lexer)
        significado = "Oración válida según la gramática del español"
        
        # Análisis semántico
        analizador = AnalizadorSemantico(lexico)
        errores_semanticos = analizador.analizar(resultado)
        
        if errores_semanticos:
            significado = "Oración sintácticamente correcta pero con errores semánticos"
        
        arbol_imagen = generar_imagen_arbol(resultado)
        arbol_imagen = '/' + arbol_imagen

    except Exception as e:
        error = f"Error al analizar: {str(e)}"

    return jsonify({
        'significado': significado,
        'arbol_imagen': arbol_imagen,
        'error': error,
        'errores_semanticos': errores_semanticos
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
    
    return jsonify({
        'palabra': word,
        'tipo': 'desconocido',
        'info': 'Esta palabra no está en nuestro diccionario'
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
