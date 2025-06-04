# arbol_grafico.py

from graphviz import Digraph
import os

def generar_imagen_arbol(arbol):
    """Genera una imagen PNG del árbol sintáctico usando Graphviz."""
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
    
    if not os.path.exists('static'):
        os.makedirs('static')
    ruta_imagen = 'static/arbol.png'
    dot.render('static/arbol', format='png', cleanup=True)
    return ruta_imagen
