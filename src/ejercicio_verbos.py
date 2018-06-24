import nltk
import verbos as vb
import oraciones as orac
from pattern.en import lexeme, lemma
from constantes import CARACTER_BLANCO
import re

def ejercicio_verbos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_verbos(data)
    return ejercicios

def procesar_ejercicio_verbos(texto, max_verbos=10):
    parrafos = texto.split('\n')
    cant_parrafos = len([p for p in parrafos if p != ''])
    posicion_inicial = 0
    cant_verbos = 0
    texto_ejercicio = []
    opciones = []
    for parrafo in parrafos:
        tokens = nltk.word_tokenize(parrafo)
        lista_verbos = vb.obtener_verbos(tokens, max_verbos//cant_parrafos)
        for idx, verbo in enumerate(lista_verbos):
            conjugaciones = lexeme(verbo['token'])
            conjugaciones = vb.filtrar_conjugaciones(verbo, conjugaciones)
            opcion = {
                'posicion': verbo['posicion'] + posicion_inicial,
                'variantes': conjugaciones,
                'solucion': verbo['token'],
                'referencia': idx + cant_verbos
            }
            opciones.append(opcion)
        texto_ejercicio.append(orac.sustituir_verbos(tokens, lista_verbos, cant_verbos))
        posicion_inicial = posicion_inicial + len(tokens)
        cant_verbos = cant_verbos + len(lista_verbos)
    ejercicio = {
        'texto': '\n'.join(texto_ejercicio),
        'opciones': opciones
    }
    eliminar_iguales(ejercicio)
    return ejercicio

def eliminar_iguales(ejercicio):
    lista_verbos = [lemma(x['solucion']) for x in ejercicio['opciones']]
    for opc in ejercicio['opciones']:
        if lista_verbos.count(lemma(opc['solucion'])) > 1:
            eliminar_verbo(ejercicio, opc['referencia'])

def eliminar_verbo(ejercicio, referencia):
    elem = [opcion for opcion in ejercicio['opciones'] if opcion['referencia'] == referencia][0]
    ejercicio['opciones'].remove(elem)
    verbo = elem['solucion']
    ejercicio['texto'] = re.sub(re.escape(formato_espacio(referencia)) + r'\(.*?\)' , verbo, ejercicio['texto'])
    for blank in ejercicio['opciones']:
        if blank['referencia'] > referencia:
            ejercicio['texto'] = ejercicio['texto'].replace(formato_espacio(blank['referencia']), formato_espacio(blank['referencia'] - 1))
            blank['referencia'] -= 1

def formato_espacio(referencia):
    return '(' + str(referencia) + ') ' + CARACTER_BLANCO
