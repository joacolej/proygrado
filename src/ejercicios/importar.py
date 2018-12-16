from ejercicios.ejercicio_use_en import EjercicioUseEn, ItemEjercicioUseEn
from ejercicios.ejercicio_sustantivos import EjercicioSustantivos, ItemEjercicioSustantivos
from ejercicios.ejercicio_verbos import EjercicioVerbos, ItemEjercicioVerbos
from ejercicios.ejercicio_hiponimos import EjercicioHiponimos, ItemEjercicioHiponimos
import procesamientos.oraciones as orac
import json
import nltk


def importar_st_modificado(dict_ex, palabra, definicion):
    items = []
    for sol in dict_ex['soluciones']:
        if palabra == sol['palabra']:
            definicion_oculta = orac.sustituir_sustantivo(nltk.word_tokenize(definicion), sol['palabra'])
            item = ItemEjercicioSustantivos(sol['palabra'], None, definicion, definicion_oculta)
        else:
            item = ItemEjercicioSustantivos(sol['palabra'], None, sol['definicion'], sol['definicion_oculta'])
        items.append(item)
    ret = EjercicioSustantivos(dict_ex['texto'], items)
    return ret


def importar_ejercicio(dict_ex):
    items = []

    if dict_ex['tipo'] == 'sustantivos':
        for sol in dict_ex['soluciones']:
            item = ItemEjercicioSustantivos(sol['palabra'], None, sol['definicion'], sol['definicion_oculta'])
            items.append(item)
        ret = EjercicioSustantivos(dict_ex['texto'], items)
    elif dict_ex['tipo'] == 'use_of_en':
        for opcion in dict_ex['opciones']:
            dicc = { '(': '', ')': '' }
            referencia = orac.sustituir_todos(opcion['referencia'], dicc)
            item = ItemEjercicioUseEn(opcion['solucion'], opcion['variantes'], referencia)
            items.append(item)
        ejercicio = {
            'texto' : dict_ex['texto'],
            'items' : items
        }
        ret = EjercicioUseEn(dict_ex['texto_original'], ejercicio)
    elif dict_ex['tipo'] == 'verbos':
        for opcion in dict_ex['opciones']:
            dicc = { '(': '', ')': '' }
            referencia = orac.sustituir_todos(opcion['referencia'], dicc)
            item = ItemEjercicioVerbos(opcion['solucion'], opcion['variantes'], referencia, opcion['posicion'], opcion['tiempo_verbal'])
            items.append(item)
        ejercicio = {
            'texto' : dict_ex['texto'],
            'items' : items
        }
        ret = EjercicioVerbos(dict_ex['texto_original'], ejercicio)
    elif dict_ex['tipo'] == 'hiponimos':
        for opcion in dict_ex['opciones']:
            item = ItemEjercicioHiponimos(opcion['palabra'], opcion['categoria'])
            items.append(item)
        ret = EjercicioHiponimos(dict_ex['texto_original'], items)

    return ret
