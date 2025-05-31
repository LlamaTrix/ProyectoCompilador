import ply.yacc as yacc
from lexico import tokens

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