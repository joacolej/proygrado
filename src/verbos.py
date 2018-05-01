import nltk
import json
from constantes import POS_TAGS_PRESENTE, POS_TAGS_PASADO_PARTICIPIO, POS_TAGS_PASADO
from procesamiento import obtener_palabras

# Importa y lee un archivo del tipo json
def abrir_json_file(ruta_texto):
    with open(ruta_texto) as data_file:
        data = json.load(data_file)
    return data

# Evalua según el pos tag si el token es un verbo
def es_verbo(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    verbo_pos_tag = 'VB'
    if (pos_tag[0:2] == verbo_pos_tag):
        return True
    return False

def es_gerundio(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    return pos_tag == 'VBG'

# Devuelve los verbos con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_verbos(tokens):
    return obtener_palabras(lambda x: es_verbo(x) and not es_gerundio(x), tokens)

def filtrar_verbos(lista_verbos):
    data = abrir_json_file('../recursos/lista_verbos_movers.json')
    for verbo in lista_verbos:
        if verbo['token'] in data['verbos']:
            lista_verbos.remove(verbo)
    return lista_verbos

def obtener_tiempo(pos_tag):
    if pos_tag in POS_TAGS_PRESENTE:
        return 'present'
    elif pos_tag in POS_TAGS_PASADO:
        return 'past'
    elif pos_tag in POS_TAGS_PASADO_PARTICIPIO:
        return 'past participle'
