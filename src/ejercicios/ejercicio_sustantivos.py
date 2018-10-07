import sys
sys.path.insert(0,'../procesamiento')

import palabras_use_en
import nltk
import sustantivos as st
import oraciones as orac
import random

# Ejercicio para matchear sustantivos con sus definiciones
def ejercicio_sustantivos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_sustantivos(data)
    return ejercicios

# Retorna los sustantivos seleccionados con su correspondiente definicion
def procesar_ejercicio_sustantivos(texto):
    tokens = nltk.word_tokenize(texto)
    lista_sustantivos = st.obtener_sustantivos(texto)
    lista_sustantivos = list({ each['token'] : each for each in lista_sustantivos }.values())
    palabras, definiciones, soluciones = ([] for i in range(3))
    for sustantivo in lista_sustantivos:
        palabras.append(sustantivo['token'])
        definicion = st.obtener_mejor_definicion(tokens, sustantivo['token'])
        definicion_tokens = nltk.word_tokenize(definicion)
        definiciones.append(orac.sustituir_sustantivo(definicion_tokens, sustantivo['token']))
        solucion = {
            'palabra': sustantivo['token'], 'definicion': definicion
        }
        soluciones.append(solucion)
    random.shuffle(palabras)
    random.shuffle(definiciones)
    ejercicio = {
        'palabras': palabras,
        'definiciones': definiciones,
        'soluciones': soluciones,
        'tipo': 'sustantivos'
    }
    return ejercicio
