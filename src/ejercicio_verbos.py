import nltk
import verbos
import oraciones
from pattern.en import conjugate, lemma, lexeme

def ejercicio_verbos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_verbos(data)
    return ejercicios

def procesar_ejercicio_verbos(texto):
    tokens = nltk.word_tokenize(texto)
    lista_verbos = verbos.obtener_verbos(tokens)
    opciones = []
    for idx, verbo in enumerate(lista_verbos):
        conjugaciones = lexeme(verbo['token'])
        opcion = {
            'posicion': idx,
            'opciones': conjugaciones,
            'solucion': verbo['token']
        }
        opciones.append(opcion)
    ejercicio = {
        'texto': oraciones.sustituir_verbos(tokens, lista_verbos),
        'opciones': opciones
    }
    return ejercicio
