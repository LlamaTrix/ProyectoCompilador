import ply.yacc as yacc
from lexico import Lexico

lexico = Lexico()
tokens = lexico.tokens

# Reglas sintácticas
def p_oracion(p):
    '''oracion : adverbio oracion
               | sujeto predicado
               | sujeto
               | predicado
               | negacion oracion
               | oracion_subordinada'''
    if len(p) == 3:
        p[0] = ('ORACION', p[1], p[2])
    else:
        p[0] = ('ORACION', p[1])

def p_sujeto(p):
    'sujeto : sintagma_nominal'
    p[0] = ('SUJETO', p[1])

def p_sintagma_nominal(p):
    '''sintagma_nominal : determinante sustantivo
                        | determinante sustantivo adjetivo
                        | determinante adjetivo sustantivo
                        | determinante
                        | pronombre sustantivo
                        | pronombre
                        | sustantivo
                        | nombre_propio'''
    if len(p) == 3:
        p[0] = ('SINTAGMA_NOMINAL', p[1], p[2])
    elif len(p) == 4:
        p[0] = ('SINTAGMA_NOMINAL', p[1], p[2], p[3])
    else:
        p[0] = ('SINTAGMA_NOMINAL', p[1])

def p_predicado(p):
    '''
    predicado : nucleo_predicado
              | nucleo_predicado complemento
              | nucleo_predicado oracion_relativa 
              | complemento_indirecto nucleo_predicado
              | complemento_indirecto nucleo_predicado complemento
              | nucleo_predicado sustantivo
              | nucleo_predicado sustantivo complemento
              | nucleo_predicado sustantivo complemento oracion
    '''
    if len(p) == 2:
        p[0] = ('PREDICADO_SIMPLE', p[1])
    elif len(p) == 5 and p[1] == 'no':
        p[0] = ('PREDICADO_NEGADO_COMPUESTO', p[1], p[2], p[3], p[4])
    elif len(p) == 4 and p[2] == 'conjuncion':
        p[0] = ('PREDICADO_SUBORDINADA', p[1], p[2], p[3])
    else:
        p[0] = ('PREDICADO_COMPLETO', p[1], p[2])


def p_nucleo_predicado(p):
    '''
    nucleo_predicado : verbo
                     | verbo nucleo_predicado
    '''
    if len(p) == 2:
        p[0] = ('NUCLEO', p[1])
    else:
        p[0] = ('NUCLEO_COMPUESTO', p[1], p[2])

def p_oracion_relativa(p):
    '''
    oracion_relativa : complemento verbo
                     | complemento pronombre verbo
    '''
    if len(p) == 3:
        p[0] = ('ORACION_RELATIVA', p[1], p[2])
    else:
        p[0] = ('ORACION_RELATIVA', p[1], p[2], p[3])

def p_oracion_subordinada(p):
    '''
    oracion_subordinada : verbo conjuncion pronombre verbo
                        | verbo conjuncion oracion
                        | verbo conjuncion predicado
                        | verbo conjuncion
    '''
    if len(p) == 5:
        if isinstance(p[4], tuple) and p[4][0] == 'ADVERBIO':
            p[0] = ('ORACION_SUBORDINADA_ADV', p[1], p[2], p[3], p[4])
        else:
            p[0] = ('ORACION_SUBORDINADA', p[1], p[2], p[3], p[4])
    else:
        p[0] = ('ORACION_SUBORDINADA_SIMPLE', p[1], p[2], p[3])

def p_complemento(p):
    '''
    complemento : complemento_simple
                | complemento complemento_simple
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('COMPLEMENTO_COMPUESTO', p[1], p[2])

def p_complemento_simple(p):
    '''
    complemento_simple : complemento_directo
                       | complemento_indirecto
                       | adverbio
                       | adjetivo
                       | conjuncion
    '''
    p[0] = ('COMPLEMENTO_SIMPLE', p[1])

def p_negacion(p):
    'negacion : NEGACION'
    p[0] = ('NEGACION', p[1])

def p_complemento_directo(p):
    'complemento_directo : sintagma_nominal'
    p[0] = ('COMPLEMENTO_DIRECTO', p[1])

def p_complemento_indirecto(p):
    '''complemento_indirecto : preposicion sintagma_nominal
                             | pronombre'''
    if len(p) == 2:
        p[0] = ('COMPLEMENTO_INDIRECTO', p[1])
    else:
        p[0] = ('COMPLEMENTO_INDIRECTO', p[1], p[2])


def p_preposicion(p):
    'preposicion : PREPOSICION'
    p[0] = ('PREPOSICION', p[1])

def p_determinante(p):
    'determinante : DETERMINANTE'
    p[0] = ('DETERMINANTE', p[1])

def p_sustantivo(p):
    'sustantivo : SUSTANTIVO'
    p[0] = ('SUSTANTIVO', p[1])

def p_verbo(p):
    'verbo : VERBO'
    p[0] = ('VERBO', p[1])

def p_adjetivo(p):
    'adjetivo : ADJETIVO'
    p[0] = ('ADJETIVO', p[1])

def p_pronombre(p):
    'pronombre : PRONOMBRE'
    p[0] = ('PRONOMBRE', p[1])

def p_nombre_propio(p):
    'nombre_propio : NOMBRE_PROPIO'
    p[0] = ('NOMBRE', p[1])

def p_adverbio(p):
    'adverbio : ADVERBIO'
    p[0] = ('ADVERBIO', p[1])

def p_conjuncion(p):
    'conjuncion : CONJUNCION'
    p[0] = ('CONJUNCION', p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en: '{p.value}'")
    else:
        print("Error de sintaxis: fin inesperado de entrada")

parser = yacc.yacc()