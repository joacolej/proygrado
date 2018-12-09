from ejercicios.ejercicio_use_en import EjercicioUseEn, ItemEjercicioUseEn
from ejercicios.ejercicio_sustantivos import EjercicioSustantivos, ItemEjercicioSustantivos
from ejercicios.ejercicio_verbos import EjercicioVerbos, ItemEjercicioVerbos
import procesamientos.oraciones as orac
import json
import nltk


def importar_ejercicio(dict_ex):
    items = []

    if dict_ex['tipo'] == 'sustantivos':
        for sol in dict_ex['soluciones']:
            definicion_oculta = (orac.sustituir_sustantivo(nltk.word_tokenize(sol['definicion']), sol['palabra']))
            item = ItemEjercicioSustantivos(sol['palabra'], None, sol['definicion'], definicion_oculta)
            items.append(item)
        ret = EjercicioSustantivos(dict_ex['texto'], items)
    elif dict_ex['tipo'] == 'use_en':
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

    return ret
