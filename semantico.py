from lexico import lexico
class AnalizadorSemantico:
    def __init__(self, lexico):
        self.errores = []
        self.genero = []
        self.lexico = lexico['palabras']
<<<<<<< HEAD
        

    def getLexico(self):
        print(self.lexico)
=======
        self.errores = []
    
    def analizar(self, arbol):
        """Analiza el árbol sintáctico y devuelve una lista de errores semánticos."""
        self.errores = []
        self._validar_arbol(arbol)
        return self.errores
    
    def _validar_arbol(self, nodo):
        """Recorre recursivamente el árbol validando cada nodo."""
        if not isinstance(nodo, tuple):
            return
        
        # La nueva estructura de ORACION es ('ORACION', elemento1, [elemento2?])
        if nodo[0] == 'ORACION':
            if len(nodo) == 3:  # Caso sujeto + predicado
                sujeto = nodo[1]
                predicado = nodo[2]
                self._validar_sujeto(sujeto)
                self._validar_predicado(predicado)
                self._validar_concordancia(sujeto, predicado)
            else:  # Caso solo sujeto o solo predicado
                componente = nodo[1]
                if componente[0] == 'SN':
                    self._validar_sujeto(componente)
                elif componente[0] == 'SV':
                    self._validar_predicado(componente)
        
        # Validar sintagmas nominales (SN) en cualquier parte del árbol
        elif nodo[0] == 'SN':
            self._validar_sintagma_nominal(nodo)
        
        # Recursión para hijos del nodo
        for hijo in nodo[1:]:
            if isinstance(hijo, (tuple, list)):
                self._validar_arbol(hijo)
    
    def _validar_sujeto(self, sujeto):
        """Valida la estructura semántica del sujeto (SN)."""
        if sujeto[0] != 'SN':
            return
        
        # Estructura esperada: ('SN', ('DET', 'el'), ('SUST', 'niño'), ...)
        if len(sujeto) < 2:
            self.errores.append("Sujeto incompleto: falta determinante o sustantivo")
            return
        
        # Validar determinante + sustantivo (si existen)
        det = None
        sust = None
        
        for elemento in sujeto[1:]:
            if elemento[0] == 'DET':
                det = elemento[1]
            elif elemento[0] == 'SUST':
                sust = elemento[1]
        
        if det and sust:
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
        """Valida la estructura semántica del predicado (SV)."""
        if predicado[0] != 'SV':
            return
        
        # Buscar el verbo en el SV
        verbo = None
        for elemento in predicado[1:]:
            if elemento[0] == 'VERBO':
                verbo = elemento
                break
        
        if not verbo:
            self.errores.append("Predicado sin verbo principal")
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
        """Valida la concordancia entre sujeto y predicado."""
        if sujeto[0] != 'SN' or predicado[0] != 'SV':
            return
        
        # Obtener información del verbo
        verbo = None
        for elemento in predicado[1:]:
            if elemento[0] == 'VERBO':
                verbo = elemento
                break
        
        if not verbo:
            return
        
        verbo_info = self._obtener_info_palabra(verbo[1], 'verbos')
        if not verbo_info:
            return
        
        # Determinar número del sujeto
        numero_sujeto = 'singular'
        genero_sujeto = 'masculino'
        
        for elemento in sujeto[1:]:
            if elemento[0] == 'DET':
                det_info = self._obtener_info_palabra(elemento[1], 'determinantes')
                if det_info:
                    numero_sujeto = det_info.get('numero', 'singular')
                    genero_sujeto = det_info.get('genero', 'masculino')
            elif elemento[0] == 'SUST':
                sust_info = self._obtener_info_palabra(elemento[1], 'sustantivos')
                if sust_info:
                    numero_sujeto = sust_info.get('numero', 'singular')
                    genero_sujeto = sust_info.get('genero', 'masculino')
            elif elemento[0] == 'PRON':
                pron_info = self._obtener_info_palabra(elemento[1], 'pronombres')
                if pron_info:
                    numero_sujeto = pron_info.get('numero', 'singular')
                    genero_sujeto = pron_info.get('genero', 'masculino')
        
        # Validar concordancia sujeto-verbo
        if verbo_info.get('numero') != numero_sujeto:
            self.errores.append(
                f"Error de concordancia: El verbo '{verbo[1]}' ({verbo_info.get('numero')}) "
                f"no concuerda en número con el sujeto ({numero_sujeto})"
            )
    
    def _validar_sintagma_nominal(self, sn):
        """Valida la estructura semántica de un sintagma nominal."""
        if sn[0] != 'SN' or len(sn) < 2:
            return
        
        # Validar adjetivos después de sustantivos
        sust = None
        for i, elemento in enumerate(sn[1:]):
            if elemento[0] == 'SUST':
                sust = elemento
                sust_info = self._obtener_info_palabra(sust[1], 'sustantivos')
                
                # Verificar adjetivos siguientes
                for adj_elemento in sn[i+2:]:
                    if adj_elemento[0] == 'ADJ':
                        adj_info = self._obtener_info_palabra(adj_elemento[1], 'adjetivos')
                        
                        if sust_info and adj_info:
                            # Validar género
                            if sust_info.get('genero') != adj_info.get('genero'):
                                self.errores.append(
                                    f"Error de género: El adjetivo '{adj_elemento[1]}' "
                                    f"no concuerda con '{sust[1]}'"
                                )
                            
                            # Validar número
                            if sust_info.get('numero') != adj_info.get('numero'):
                                self.errores.append(
                                    f"Error de número: El adjetivo '{adj_elemento[1]}' "
                                    f"no concuerda con '{sust[1]}'"
                                )
    
    def _obtener_info_palabra(self, palabra, categoria=None):
        """Busca una palabra en el léxico y devuelve sus características."""
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
>>>>>>> main
    

analz = AnalizadorSemantico(lexico)

analz.getLexico()
