import nltk
from nltk.stem import WordNetLemmatizer
from procesamiento import obtener_palabras, flatten
import sustantivos as st
import verbos as vb
from modelo_lenguaje import score_texto
from embeddings import Embeddings
from lista_de_frecuencia import Frecuencia
from utils import abrir_json_file


def seleccionar_palabras(tokens, lista_palabras = None, limite = 1):
    lista = st.obtener_sustantivos(tokens) + vb.obtener_verbos(tokens)
    if not lista_palabras is None:
        lista = [palabra for palabra in lista if palabra['token'].WordNetLemmatizer() in lista_palabras]
    frec = Frecuencia()
    return frec.ordenar_por_frecuencia(lista)[0:limite]

# TODO: problema de palabras duplicadas
def filtrar_palabras(palabra, opciones, oracion, cant_palabras=3):
    palabra_score = score_texto(oracion)
    # Las mejores opciones son las que tienen mas distancia en el score
    mejores_opciones = []
    for opcion in opciones:
        texto_opcion = oracion.replace(palabra, opcion)
        opcion_score = score_texto(texto_opcion)
        score_diferencia = palabra_score - opcion_score
        mejores_opciones.append((opcion, score_diferencia))
    mejores_opciones.sort(key=lambda x: x[1])
    mejores_opciones_sorted = list(reversed(mejores_opciones))
    return mejores_opciones_sorted[0:cant_palabras]

def obtener_sustativos_movers(palabra, oracion):
    data = abrir_json_file('../recursos/lista_palabras_movers.json')
    palabras_movers = data['palabras']
    sustantivos_movers = []
    for palabra_movers in palabras_movers:
        texto_opcion = oracion.replace(palabra, palabra_movers)
        texto_tokenized = nltk.word_tokenize(texto_opcion)
        tokens = nltk.pos_tag(texto_tokenized)
        # Encontrar si el token es un sustantivo
        es_sustantivo = False
        for token in tokens:
            es_sustantivo = es_sustantivo | (token[1][0:2] == 'NN')
        if es_sustantivo:
            sustantivos_movers.append(palabra_movers)
    return sustantivos_movers

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
