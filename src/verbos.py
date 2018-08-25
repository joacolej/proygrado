# coding=utf-8
import nltk
import random
from constantes import POS_TAGS_PRESENTE, POS_TAGS_PASADO_PARTICIPIO, POS_TAGS_PASADO
from procesamiento import obtener_palabras
from pattern.en import tenses, PAST, PRESENT
from utils import abrir_json_file

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
def obtener_verbos(texto):
    return obtener_palabras(lambda x: es_verbo(x) and not es_gerundio(x), texto)

def filtrar_verbos(lista_verbos):
    data = abrir_json_file('../recursos/lista_palabras_movers.json')
    for verbo in lista_verbos:
        if verbo['token'] in data['palabras']:
            lista_verbos.remove(verbo)
    return lista_verbos

def filtrar_conjugaciones(verbo, conjugaciones):
    conjugaciones = [x for x in conjugaciones if "n't" not in x and "not" not in x]
    if len(conjugaciones) <= 4:
        return conjugaciones
    else:
        if verbo['pos_tag'] in POS_TAGS_PRESENTE:
            conjugaciones = [x for x in conjugaciones if PAST not in tenses(x)]
        elif verbo['pos_tag'] in POS_TAGS_PASADO:
            conjugaciones = [x for x in conjugaciones if is_not_present(x)]
        if len(conjugaciones) >= 4:
            conjugaciones.remove(omitir_contraccion(verbo['token']))
            conjugaciones = random.sample(conjugaciones, 3)
            conjugaciones.append(verbo['token'])
        return conjugaciones

def omitir_contraccion(verbo):
    if verbo == "'s":
        return 'is'
    elif verbo == "'m":
        return 'am'
    elif verbo == "'re":
        return 'are'
    else:
        return verbo

def is_not_present(conjugacion):
    return (PRESENT, 1) not in tenses(conjugacion) and (PRESENT, 2) not in tenses(conjugacion) and (PRESENT, 3) not in tenses(conjugacion)

def obtener_tiempo(pos_tag):
    if pos_tag in POS_TAGS_PRESENTE:
        return 'present'
    elif pos_tag in POS_TAGS_PASADO:
        return 'past'
    elif pos_tag in POS_TAGS_PASADO_PARTICIPIO:
        return 'past participle'
