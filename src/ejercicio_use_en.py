import nltk
from random import shuffle
import sustantivos as st
import oraciones as orac
import palabras_use_en as use_en
import itertools
from procesamiento import parse_pos_tags

# Ejercicio para matchear sustantivos con sus definiciones
def ejercicio_use_en(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_use_en(data)
    return ejercicios

# Retorna los sustantivos seleccionados con su correspondiente definicion
def procesar_use_en(texto):
    opciones = []
    texto_ejercicio = []
    oraciones = orac.separar_oraciones(texto)
    referencia = itertools.count()
    palabras_usadas = []
    for oracion in oraciones:
        tokens = nltk.word_tokenize(oracion)
        lista_palabras = use_en.seleccionar_palabras(oracion, palabras_usadas=palabras_usadas)
        for palabra in lista_palabras:
            referencia_actual = next(referencia)
            variantes = use_en.filtro_categoria_movers(palabra)
            variantes = use_en.filtro_similaridad(palabra['token'], variantes)
            variantes_finales = use_en.filtrar_palabras(palabra['token'], variantes, oracion)
            variantes_finales.append(palabra['token'])
            shuffle(variantes_finales)
            opcion = {
                'variantes': variantes_finales,
                'solucion': palabra['token'],
                'referencia': '(' + str(referencia_actual) + ')'
            }
            palabras_usadas.append(palabra['token'])
            texto_ejercicio.append(orac.sustituir_palabra(oracion, palabra['token'], referencia_actual))
            opciones.append(opcion)
    ejercicio = {
        'texto': '\n'.join(texto_ejercicio),
        'opciones': opciones,
        'tipo': 'use_of_en'
    }
    return ejercicio
