import nltk
import sustantivos as st
import oraciones as orac

#Ejercicio pendiente
def ejercicio_sustantivos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_sustantivos(data)
    return ejercicios

#Ejercicio pendiente
def procesar_ejercicio_sustantivos(texto):
    return []
