# coding=utf-8

from procesamientos.procesamiento import obtener_palabras

# Evalua según el pos tag si el token es una preposicion
def es_preposicion(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    preposicion_pos_tag = 'IN'
    if (pos_tag[0:2] == preposicion_pos_tag):
        return True
    return False

# Devuelve los verbos con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_preposiciones(texto):
    return obtener_palabras(lambda x: es_preposicion(x), texto)
