class AnalizadorSemantico:
    def __init__(self, lexico):
        self.lexico = lexico['palabras']
        self.errores = []
    
    def analizar(self, arbol):
        self.errores = []
        self._validar_arbol(arbol)
        return self.errores
    
    def _validar_arbol(self, nodo):
        if not isinstance(nodo, tuple):
            return
        
        if nodo[0] == 'ORACION':
            sujeto = nodo[1]
            predicado = nodo[2]
            self._validar_sujeto(sujeto)
            self._validar_predicado(predicado)
            self._validar_concordancia(sujeto, predicado)
        
        elif nodo[0] == 'SN':
            self._validar_sintagma_nominal(nodo)
        
        for hijo in nodo[1:]:
            self._validar_arbol(hijo)
    
    def _validar_sujeto(self, sujeto):
        sn = sujeto[1]
        if len(sn) < 2:
            return
        
        # Validar determinante + sustantivo
        if sn[0][0] == 'DET' and sn[1][0] == 'SUST':
            det = sn[0][1]
            sust = sn[1][1]
            
            # Obtener características
            det_info = self._obtener_info_palabra(det, 'determinantes')
            sust_info = self._obtener_info_palabra(sust, 'sustantivos')
            
            if det_info and sust_info:
                # Validar género
                if det_info.get('genero') != sust_info.get('genero'):
                    self.errores.append(
                        f"Error de género: '{det}' ({det_info.get('genero')}) "
                        f"no concuerda con '{sust}' ({sust_info.get('genero')})"
                    )
                
                # Validar número
                if det_info.get('numero') != sust_info.get('numero'):
                    self.errores.append(
                        f"Error de número: '{det}' ({det_info.get('numero')}) "
                        f"no concuerda con '{sust}' ({sust_info.get('numero')})"
                    )
    
    def _validar_predicado(self, predicado):
        verbo = predicado[1]
        if verbo[0] != 'VERBO':
            return
        
        verbo_info = self._obtener_info_palabra(verbo[1], 'verbos')
        if not verbo_info:
            return
        
        # Validar que el verbo no esté en infinitivo cuando hay sujeto explícito
        if verbo_info.get('tiempo') == 'infinitivo' and len(predicado) > 1:
            self.errores.append(
                f"Error: El verbo '{verbo[1]}' está en infinitivo pero hay sujeto explícito"
            )
    
    def _validar_concordancia(self, sujeto, predicado):
        verbo = predicado[1]
        if verbo[0] != 'VERBO':
            return
        
        verbo_info = self._obtener_info_palabra(verbo[1], 'verbos')
        if not verbo_info:
            return
        
        sn_sujeto = sujeto[1]
        numero_sujeto = 'singular'
        
        # Determinar número del sujeto
        if len(sn_sujeto) > 1 and sn_sujeto[0][0] == 'DET':
            det_info = self._obtener_info_palabra(sn_sujeto[0][1], 'determinantes')
            if det_info:
                numero_sujeto = det_info.get('numero', 'singular')
        elif sn_sujeto[0][0] == 'PRON':
            pron_info = self._obtener_info_palabra(sn_sujeto[0][1], 'pronombres')
            if pron_info:
                numero_sujeto = pron_info.get('numero', 'singular')
        
        # Validar concordancia sujeto-verbo (simplificado)
        if verbo_info.get('tiempo') != 'infinitivo':
            if 'plural' in verbo[1] and numero_sujeto == 'singular':
                self.errores.append(
                    f"Error de concordancia: El verbo '{verbo[1]}' parece plural "
                    f"pero el sujeto es singular"
                )
            elif 'singular' in verbo[1] and numero_sujeto == 'plural':
                self.errores.append(
                    f"Error de concordancia: El verbo '{verbo[1]}' parece singular "
                    f"pero el sujeto es plural"
                )
    
    def _validar_sintagma_nominal(self, sn):
        if len(sn) < 2:
            return
        
        # Validar adjetivo después de sustantivo
        if len(sn) > 2 and sn[1][0] == 'SUST' and sn[2][0] == 'ADJ':
            sust = sn[1][1]
            adj = sn[2][1]
            
            sust_info = self._obtener_info_palabra(sust, 'sustantivos')
            adj_info = self._obtener_info_palabra(adj, 'adjetivos')
            
            if sust_info and adj_info:
                # Validar género adjetivo
                if sust_info.get('genero') != adj_info.get('genero'):
                    self.errores.append(
                        f"Error de género: El adjetivo '{adj}' no concuerda "
                        f"en género con '{sust}'"
                    )
                
                # Validar número adjetivo
                if sust_info.get('numero') != adj_info.get('numero'):
                    self.errores.append(
                        f"Error de número: El adjetivo '{adj}' no concuerda "
                        f"en número con '{sust}'"
                    )
    
    def _obtener_info_palabra(self, palabra, categoria=None):
        if categoria:
            if categoria in self.lexico and palabra in self.lexico[categoria]:
                return self.lexico[categoria][palabra]
        else:
            for cat in self.lexico.values():
                if palabra in cat:
                    return cat[palabra]
        return None

# Función para generar el árbol visual (se mantiene igual)
def generar_imagen_arbol(arbol):
    from graphviz import Digraph
    import os
    
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