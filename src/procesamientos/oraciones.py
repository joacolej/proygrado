# coding=utf-8

import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from pattern.en import pluralize, singularize
import verbos as vb
from constantes import CARACTER_BLANCO

# Función que separa un texto en oraciones
def separar_oraciones(texto):
    # importar el tokenizador de oraciones de nltk
    detector_oraciones = nltk.data.load('tokenizers/punkt/english.pickle')
    oraciones = detector_oraciones.tokenize(texto)
    return oraciones

def sustituir_verbos(tokens, verbos, corrimiento):
    for idx, verbo in enumerate(verbos):
        tiempo_verbal = vb.obtener_tiempo(verbo['pos_tag'])
        tokens[verbo['posicion']] = '(' + str(idx + corrimiento) + ') ' + CARACTER_BLANCO + '(' + tiempo_verbal + ')'
    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(tokens)

def sustituir_sustantivo(tokens, sustantivo):
    tokens = [CARACTER_BLANCO if es_la_misma_palabra(x.lower(), sustantivo.lower()) else x for x in tokens]
    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(tokens)

def sustituir_palabra(oracion, palabra, idx):
    oracion_sustituida = oracion.replace(palabra, '(' + str(idx) + ') ' + CARACTER_BLANCO, 1)
    return oracion_sustituida

def sustituir_referencia(oracion, idx, palabra):
    oracion_sustituida = oracion.replace('(' + str(idx) + ') ' + CARACTER_BLANCO, palabra, 1)
    return oracion_sustituida
    
def es_la_misma_palabra(x, sustantivo):
    return (x == singularize(sustantivo) or x == pluralize(singularize(sustantivo)))

def sustituir_todos(texto, dicc):
    for i, j in dicc.iteritems():
        texto = texto.replace(i, j, 1)
    return texto
