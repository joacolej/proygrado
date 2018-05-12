import nltk
from nltk.tokenize.moses import MosesDetokenizer
from pattern.en import pluralize, singularize

import verbos as vb
from constantes import CARACTER_BLANCO

# Función que separa un texto en oraciones
def separar_oraciones(texto):
    # importar el tokenizador de oraciones de nltk
    detector_oraciones = nltk.data.load('tokenizers/punkt/english.pickle')
    oraciones = detector_oraciones.tokenize(texto)
    return oraciones

def sustituir_verbos(tokens, verbos):
    for idx, verbo in enumerate(verbos):
        tiempo_verbal = vb.obtener_tiempo(verbo['pos_tag'])
        tokens[verbo['posicion']] = str(idx) + ') ' + CARACTER_BLANCO + '(' + tiempo_verbal + ')'
    detokenizer = MosesDetokenizer()
    return detokenizer.detokenize(tokens, return_str=True)

def sustituir_sustantivo(tokens, sustantivo):
    tokens = [CARACTER_BLANCO if es_la_misma_palabra(x.lower(), sustantivo.lower()) else x for x in tokens]
    detokenizer = MosesDetokenizer()
    return detokenizer.detokenize(tokens, return_str=True)
    
def es_la_misma_palabra(x, sustantivo):
    return (x == singularize(sustantivo) or x == pluralize(singularize(sustantivo)))
