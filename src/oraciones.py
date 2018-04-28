import nltk
from nltk.tokenize.moses import MosesDetokenizer

import verbos as vb
from constantes import CARACTER_BLANCO

# Función que separa un texto en oraciones
def separar_oraciones(texto):
    # importar el tokenizador de oraciones de nltk
    detector_oraciones = nltk.data.load('tokenizers/punkt/english.pickle')
    oraciones = detector_oraciones.tokenize(texto)
    return oraciones

def sustituir_verbos(tokens, verbos):
    for verbo in verbos:
        tiempo_verbal = vb.obtener_tiempo(verbo['pos_tag'])
        tokens[verbo['posicion']] = CARACTER_BLANCO + ' (' + tiempo_verbal + ')'
    detokenizer = MosesDetokenizer()
    return detokenizer.detokenize(tokens, return_str=True)
