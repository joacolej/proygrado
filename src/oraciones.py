import nltk

# Función que separa un texto en oraciones
def separar_oraciones(texto):
    # importar el tokenizador de oraciones de nltk
    detector_oraciones = nltk.data.load('tokenizers/punkt/english.pickle')
    oraciones = detector_oraciones.tokenize(texto)
    return oraciones
