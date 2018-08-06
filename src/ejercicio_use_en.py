import nltk
import sustantivos as st
import oraciones as orac
import palabras_use_en as use_en

# Ejercicio para matchear sustantivos con sus definiciones
def ejercicio_use_en(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_use_en(data)
    return ejercicios

# Retorna los sustantivos seleccionados con su correspondiente definicion
def procesar_use_en(texto):
    opciones = []
    oraciones = orac.separar_oraciones(texto)
    for oracion in oraciones:
        tokens = nltk.word_tokenize(oracion)
        lista_palabras = use_en.seleccionar_palabras(tokens)
        for palabra in lista_palabras:
            opciones = obtener_opciones(palabra, oracion)
    return ejercicio
