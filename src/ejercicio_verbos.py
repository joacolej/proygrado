import nltk
import verbos as vb
import oraciones as orac
from pattern.en import lexeme

def ejercicio_verbos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_verbos(data)
    return ejercicios

def procesar_ejercicio_verbos(texto):
    tokens = nltk.word_tokenize(texto)
    lista_verbos = vb.obtener_verbos(tokens)
    opciones = []
    for idx, verbo in enumerate(lista_verbos):
        conjugaciones = lexeme(verbo['token'])
        opcion = {
            'posicion': verbo['posicion'],
            'variantes': conjugaciones,
            'solucion': verbo['token'],
            'referencia': str(idx) + ')'
        }
        opciones.append(opcion)
    ejercicio = {
        'texto': orac.sustituir_verbos(tokens, lista_verbos),
        'opciones': opciones
    }
    return ejercicio
