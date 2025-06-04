import json
import difflib

class Semantico:
    def __init__(self):
        self.datos = self.cargar_json()

    def cargar_json(self):
        try:
            with open('semantico.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar semantico.json: {str(e)}")
            return {"phrases": {}}

    def buscar_significado(self, oracion):
        frases = self.datos.get("phrases", {})
        if oracion in frases:
            return frases[oracion]
        else:
            similares = difflib.get_close_matches(oracion, frases.keys(), n=1, cutoff=0.6)
            if similares:
                return f"No se encontró un significado exacto. ¿Quisiste decir '{similares[0]}'? -> {frases[similares[0]]}"
            else:
                return "No se encontró un significado similar."
