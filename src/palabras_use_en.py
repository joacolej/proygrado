import nltk
from procesamiento import obtener_palabras, flatten
import sustantivos as st
from modelo_lenguaje import score_texto
from embeddings import obtener_palabras_similares

def seleccionar_palabras(tokens):
    return st.obtener_sustantivos(tokens)

# TODO: problema de palabras duplicadas
def filtrar_palabras(palabra, opciones, oracion, cant_palabras=3):
    palabra_score = score_texto(oracion)
    mejores_opciones = []
    for opcion in opciones:
        texto_opcion = oracion.replace(palabra, opcion)
        opcion_score = score_texto(texto_opcion)
        score_diferencia = opcion_score - palabra_score
        mejores_opciones.append((opcion, score_diferencia))
    return sorted(mejores_opciones)[0:cant_palabras]

# Funcion que retorna 3 opciones similares pero con baja probabilidad en el modelo de lenguaje
def obtener_opciones(palabra, oracion):
    opciones_posibles = obtener_palabras_similares(palabra)
    opciones = filtrar_palabras(palabra, opciones_posibles, oracion)
    return opciones
