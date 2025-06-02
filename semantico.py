class AnalizadorSemantico:
    def __init__(self, lexico, semantica=None):
        self.lexico = lexico['palabras']
        self.semantica = semantica or {}
        self.errores = []
    
    def _validar_concordancia_genero_numero(self, palabra1, palabra2, categoria1, categoria2):
        """Valida concordancia de genero y numero entre dos palabras"""
        info1 = self._obtener_info_palabra(palabra1, categoria1)
        info2 = self._obtener_info_palabra(palabra2, categoria2)
        
        if not info1 or not info2:
            return
            
        genero1 = info1.get('genero')
        genero2 = info2.get('genero')
        
        if genero1 and genero2 and genero1 != 'neutral' and genero2 != 'neutral':
            if genero1 != genero2:
                self.errores.append(
                    f"Error de genero: '{palabra1}' ({genero1}) no concuerda con '{palabra2}' ({genero2})"
                )
        
        numero1 = info1.get('numero')
        numero2 = info2.get('numero')
        
        if numero1 and numero2 and numero1 != numero2:
            self.errores.append(
                f"Error de numero: '{palabra1}' ({numero1}) no concuerda con '{palabra2}' ({numero2})"
            )
    
    def _validar_concordancia_sujeto_verbo(self, sujeto, verbo):
        """Valida concordancia entre sujeto y verbo en persona y numero"""
        info_verbo = self._obtener_info_palabra(verbo, 'verbos')
        if not info_verbo:
            return
            
        persona_sujeto = self._obtener_persona_sujeto(sujeto)
        numero_sujeto = self._obtener_numero_sujeto(sujeto)
        
        if info_verbo.get('persona') != persona_sujeto:
            self.errores.append(
                f"Error de concordancia: El verbo '{verbo}' no concuerda en persona con el sujeto"
            )
            
        if info_verbo.get('numero') != numero_sujeto:
            self.errores.append(
                f"Error de concordancia: El verbo '{verbo}' no concuerda en numero con el sujeto"
            )
    
    def _obtener_persona_sujeto(self, sujeto):
        """Determina la persona gramatical del sujeto"""
        if sujeto[0] == 'SUJETO':
            sn = sujeto[1]
            if sn[0] == 'SN':
                if len(sn) > 1 and sn[1][0] == 'PRON':
                    pron_info = self._obtener_info_palabra(sn[1][1], 'pronombres')
                    return pron_info.get('persona') if pron_info else 'tercera'
                else:
                    return 'tercera'  
        return 'tercera'
    
    def _obtener_numero_sujeto(self, sujeto):
        """Determina el numero gramatical del sujeto"""
        if sujeto[0] == 'SUJETO':
            sn = sujeto[1]
            if sn[0] == 'SN':
                if len(sn) > 1 and sn[1][0] == 'PRON':
                    pron_info = self._obtener_info_palabra(sn[1][1], 'pronombres')
                    return pron_info.get('numero') if pron_info else 'singular'
                elif len(sn) > 2 and sn[1][0] == 'DET':
                    det_info = self._obtener_info_palabra(sn[1][1], 'determinantes')
                    return det_info.get('numero') if det_info else 'singular'
                elif len(sn) > 1 and sn[2][0] == 'SUST':
                    sust_info = self._obtener_info_palabra(sn[2][1], 'sustantivos')
                    return sust_info.get('numero') if sust_info else 'singular'
        return 'singular'
    
    def _validar_arbol(self, nodo):
        if not isinstance(nodo, tuple):
            return
        
        if nodo[0] == 'ORACION':
            sujeto = nodo[1]
            predicado = nodo[2]
            
            # Validar concordancia sujeto-verbo
            if predicado[0] == 'PREDICADO' and len(predicado) > 1:
                verbo = predicado[1]
                if verbo[0] == 'VERBO':
                    self._validar_concordancia_sujeto_verbo(sujeto, verbo[1])
            
            self._validar_sujeto(sujeto)
            self._validar_predicado(predicado)
        
        for hijo in nodo[1:]:
            self._validar_arbol(hijo)
    
    def analizar_semantica_femenina(self, oracion_texto):
        """Analiza si una oracion tiene un significado oculto segun el diccionario semantico"""
        significado_oculto = self.semantica.get(oracion_texto.strip())
        
        if significado_oculto:
            return {
                "tiene_significado_oculto": True,
                "significado_literal": oracion_texto,
                "significado_real": significado_oculto["significado"]
            }
        else:
            return {
                "tiene_significado_oculto": False,
                "significado_literal": oracion_texto,
                "significado_real": oracion_texto
            }