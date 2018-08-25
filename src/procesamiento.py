# coding=utf-8

import nltk
from nltk.corpus import wordnet as wordnet
from pattern.en import tag

# Toma un texto taggeado y devuelve una lista que contiene "token, pos_tags, posicion_palabra"
def parse_pos_tags(pos_tags):
    return [{ 'token':t, 'pos_tag':p, 'posicion':i } for i,(t,p) in enumerate(pos_tags)]

# Devuelve las palabras con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_palabras(filtro, texto):
    pos_tags = tag(texto)
    pos_tags_con_posiciones = parse_pos_tags(pos_tags)
    palabras = list(filter(filtro, pos_tags_con_posiciones))
    return palabras

def tiene_igual_synset(palabra, pos_tag):
    synsets = wordnet.synsets(palabra) 
    return any(synset.pos() == pos_tag and palabra in synset.lemma_names() for synset in synsets)

def serialize_ojectid(lista):
    results = []
    for document in lista:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results

def obtener_frecuencias(texto):
    frecuencias = {}
    tokens = nltk.word_tokenize(texto)
    tokens = list(filter(lambda x: x != '.' and x != ',' and x != ';', tokens))
    frecuencias = { i:tokens.count(i) for i in set(tokens) }
    return frecuencias

def flatten(lista):
    lista_plana = []
    for sublista in lista:
        if isinstance(sublista, list):
            for item in sublista:
                lista_plana.append(item)
        else:
            lista_plana.append(sublista)
    return lista_plana
