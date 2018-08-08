import nltk
from procesamiento import obtener_palabras, flatten
import sustantivos as st
from modelo_lenguaje import score_texto
from embeddings import Embeddings

def seleccionar_palabras(tokens):
    return st.obtener_sustantivos(tokens)

# TODO: problema de palabras duplicadas
def filtrar_palabras(palabra, opciones, oracion, cant_palabras=3):
    palabra_score = score_texto(oracion)
    # Las mejores opciones son las que tienen mas distancia en el score
    mejores_opciones = []
    for opcion in opciones:
        texto_opcion = oracion.replace(palabra, opcion)
        opcion_score = score_texto(texto_opcion)
        score_diferencia = opcion_score - palabra_score
        mejores_opciones.append((opcion, score_diferencia))
    print(mejores_opciones)
    return list(reversed(sorted(mejores_opciones)))[0:cant_palabras]

# Funcion que retorna 3 opciones similares pero con baja probabilidad en el modelo de lenguaje
def obtener_opciones(palabra, oracion):
    # Obtenemos palabras similares de word embeddings.
    # Lo retornado tiene sentido
    # Problemas:
    # 1. Para sustantivos a veces devuelve palabras demasiado parecidas -> no aplica al ejercicio
    # 2. Palabras poco conocidas o poco frecuentes
    # Posibles soluciones:
    # 1. Cambiar configuracion de word embeddings (incluyendo cambio de corpus)
    # 2. Agregar palabras por fuera de word embeddings (palabras frecuentes y lista generada) y testearlas con el modelo de lenguaje
    modelo_embeddings = Embeddings('wiki-simple')
    tuplas_posibles = modelo_embeddings.obtener_palabras_similares(palabra)    

    opciones_posibles = [tupla[0] for tupla in tuplas_posibles]
    opciones = filtrar_palabras(palabra, opciones_posibles, oracion)
    return opciones
