import nltk
from nltk.stem import WordNetLemmatizer
from procesamiento import flatten, tiene_igual_synset, parse_pos_tags
import sustantivos as st
import verbos as vb
from modelo_lenguaje import score_texto
from embeddings import Embeddings
from utils import abrir_json_file, postag_a_synset
from lista_de_frecuencia import Frecuencia
from pattern.en import tag, conjugate, PAST, FUTURE

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

def obtener_categoria_palabras(palabra):
    if (vb.es_verbo(palabra)):
        return 'verbos'
    return 'sustantivos'

def filtro_pos_tagger(palabra, oracion):
    data = abrir_json_file('../recursos/lista_palabras_movers.json')
    categoria_palabras_movers = obtener_categoria_palabras(palabra)
    palabras_movers = data[categoria_palabras_movers]
    opciones_movers = []
    palabra_synset = postag_a_synset(palabra['pos_tag'])
    for palabra_movers in palabras_movers:
        texto_opcion = oracion.replace(palabra['token'], palabra_movers)
        pos_tags = tag(texto_opcion)
        parsed_pos_tag = parse_pos_tags(pos_tags)
        # Encontrar si el token pertenece a la misma clase que la palabra
        descartar_palabra = False
        es_verbo = False
        for word in parsed_pos_tag:
            if word['token'] == palabra_movers:
                es_verbo = vb.es_verbo(word)
                # Obtenemos el valor de la palabra a procesar
                if (es_verbo):
                    es_verbo_presente = vb.obtener_tiempo(word['pos_tag']) == 'present'
                    # Descartar distractor si no es verbo en presente
                    if (not es_verbo_presente):
                        descartar_palabra = True
                    distractor = vb.verbo_a_infinitivo(word['token'])
                    if (word['pos_tag'][0:2] != palabra['pos_tag'][0:2]):
                        descartar_palabra = True
                else:
                    distractor = palabra_movers
                    # Descartar si el pos tag del distractor y de la opcion coinciden
                    if (word['pos_tag'] != palabra['pos_tag']):
                        descartar_palabra = True

                if (not descartar_palabra):
                    descartar_palabra = not tiene_igual_synset(distractor, palabra_synset)
        if not descartar_palabra:
            if (es_verbo):
                tiempo_opcion = vb.obtener_tiempo(palabra['pos_tag'])
                distractor_conjugado = vb.conjugar_verbo(palabra_movers, tiempo_opcion)
                opciones_movers.append(distractor_conjugado)
            else:
                opciones_movers.append(palabra_movers)
    return opciones_movers

def filtro_categoria_movers(palabra):
    data = abrir_json_file('../recursos/lista_palabras_movers.json')
    categoria_palabras_movers = obtener_categoria_palabras(palabra)
    palabras_movers = data[categoria_palabras_movers]
    opciones_movers = []
    es_verbo = vb.es_verbo(palabra)
    for palabra_movers in palabras_movers:
        if (es_verbo):
            tiempo_opcion = vb.obtener_tiempo(palabra['pos_tag'])
            distractor_conjugado = vb.conjugar_verbo(palabra_movers, tiempo_opcion)
            opciones_movers.append(distractor_conjugado)
        else:
            opciones_movers.append(palabra_movers)
    return opciones_movers

def filtro_similaridad(palabra, distractores, cota_similaridad = 0.3, minimo_a_retornar = 3):
    modelo_embeddings = Embeddings('../recursos/modelos/wiki-simple.model')
    todas_variantes = []
    variantes = []
    for distractor in distractores:
        similarity = modelo_embeddings.similarity(palabra, distractor)
        todas_variantes.append((distractor, similarity))
        if (similarity > cota_similaridad):
            variantes.append(distractor)
    if (len(variantes) >= minimo_a_retornar):
        return variantes
    todas_variantes.sort(key=lambda x: x[1])
    mejores_variantes = list(reversed(todas_variantes))
    return map(lambda x: x[0], mejores_variantes[0:3])

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
