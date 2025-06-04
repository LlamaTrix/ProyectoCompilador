from flask import Flask, render_template, request, jsonify
from lexico import Lexico
from sintactico import parser
from generar_arbol import generar_imagen_arbol
from semantico import Semantico
import random
import json

app = Flask(__name__)
lexico = Lexico()
semantico = Semantico()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}
    if request.method == "POST":
        oracion = request.form.get("frase", "").strip()
        if oracion:
            resultado_lexico = lexico.analizar(oracion)
            tokens = resultado_lexico.get("tokens", [])
            errores_lexicos = resultado_lexico.get("error_lexico", [])

            if not errores_lexicos:
                try:
                    arbol = parser.parse(oracion)
                    if arbol:
                        ruta_imagen = generar_imagen_arbol(arbol)
                        significado = semantico.buscar_significado(oracion)
                        resultado.update({
                            "tokens": [f"{t.type}: {t.value}" for t in tokens],
                            "valido": True,
                            "arbol_img": ruta_imagen,
                            "significado": significado,
                        })
                    else:
                        resultado["valido"] = False
                        resultado["error_sintactico"] = "Estructura inválida o incompleta."
                except Exception as e:
                    resultado["valido"] = False
                    resultado["error_sintactico"] = f"Error de análisis sintáctico: {str(e)}"
            else:
                resultado["valido"] = False
                resultado["tokens"] = [f"{t.type}: {t.value}" for t in tokens]
                resultado["error_lexico"] = errores_lexicos

    diccionario = lexico.obtener_diccionario_clasificado()
    return render_template("index.html", resultado=resultado, diccionario=diccionario)

@app.route("/frase-ejemplo")
def frase_ejemplo():
    try:
        with open("semantico.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            frases = list(data.get("phrases", {}).keys())
            if frases:
                frase = random.choice(frases)
                return jsonify({"frase": frase})
            else:
                return jsonify({"error": "No hay frases disponibles"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
