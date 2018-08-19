import nltk
import sustantivos as st
import oraciones as orac
import palabras_use_en as use_en
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
    for oracion in oraciones:
        tokens = nltk.word_tokenize(oracion)
        tokens_tagged = nltk.pos_tag(tokens)
        lista_palabras = use_en.seleccionar_palabras(tokens)
        for idx, palabra in enumerate(lista_palabras):
            palabra_tag = [item for item in tokens_tagged if item[0] == palabra][0] 
            variantes = use_en.obtener_opciones_movers(palabra_tag, oracion)
            variantes_finales = use_en.filtrar_palabras(palabra, variantes, oracion)
            opcion = {
                'variantes': variantes_finales,
                'solucion': palabra,
                'referencia': '(' + str(idx) + ')'
            }
            texto_ejercicio.append(orac.sustituir_palabra(tokens, palabra, idx))
            opciones.append(opcion)
    ejercicio = {
        'texto': '\n'.join(texto_ejercicio),
        'opciones': opciones,
        'tipo': 'use_of_en'
    }
    return ejercicio
