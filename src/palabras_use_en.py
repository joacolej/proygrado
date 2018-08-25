import nltk
from nltk.stem import WordNetLemmatizer
from procesamiento import flatten, tiene_igual_synset
import sustantivos as st
import verbos as vb
from modelo_lenguaje import score_texto
from embeddings import Embeddings
from utils import abrir_json_file, postag_a_synset
from lista_de_frecuencia import Frecuencia

frec = Frecuencia()

def seleccionar_palabras(oracion, lista_palabras = None, limite = 1):
    lista = st.obtener_sustantivos(oracion) + vb.obtener_verbos(oracion)
    if not lista_palabras is None:
        lista = [palabra for palabra in lista if palabra['token'].WordNetLemmatizer() in lista_palabras]
    return frec.ordenar_por_frecuencia(lista)[0:limite]

# TODO: problema de palabras duplicadas
def filtrar_palabras(palabra, opciones, oracion, cant_palabras=3):

    tokens = nltk.word_tokenize(oracion)
    tokens = list(filter(lambda x: x != '.' and x != ',' and x != ';', tokens))
    oracion_sin_puntuacion = ' '.join(tokens)

    palabra_score = score_texto(oracion_sin_puntuacion)
    # Las mejores opciones son las que tienen mas distancia en el score
    mejores_opciones = []
    for opcion in opciones:
        texto_opcion = oracion_sin_puntuacion.replace(palabra, opcion)
        opcion_score = score_texto(texto_opcion)
        score_diferencia = palabra_score - opcion_score
        mejores_opciones.append((opcion, score_diferencia))
    mejores_opciones.sort(key=lambda x: x[1])
    mejores_opciones_sorted = list(reversed(mejores_opciones))
    mejores_opciones_sorted = [elem[0] for elem in mejores_opciones_sorted]
    return mejores_opciones_sorted[0:cant_palabras]

def filtrar_opciones_por_frecuencia(opciones):
    mejores_por_frecuencia = []
    opciones_ordenadas = frec.ordenar_por_frecuencia(opciones)
    mejores_por_frecuencia = opciones_ordenadas[:10]
    return mejores_por_frecuencia

def obtener_opciones_movers(pos_tag, oracion):
    data = abrir_json_file('../recursos/lista_palabras_movers.json')
    palabras_movers = data['palabras']
    opciones_movers = []
    palabra_synset = postag_a_synset(pos_tag)
    for palabra_movers in palabras_movers:
        # Encontrar si el token pertenece a la misma clase que la palabra
        igual_categoria = tiene_igual_synset(palabra_movers, palabra_synset)
        if igual_categoria:
            opciones_movers.append(palabra_movers)
    return opciones_movers

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
