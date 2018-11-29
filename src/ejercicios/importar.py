from ejercicios.ejercicio_use_en import EjercicioUseEn, ItemEjercicioUseEn
from ejercicios.ejercicio_sustantivos import EjercicioSustantivos, ItemEjercicioSustantivos
import procesamientos.oraciones as orac
import json
import nltk


def importar_ejercicio(json_ex):
    dict_ex = json.loads(json_ex)
    items = []

    if dict_ex['tipo'] == 'sustantivos':
        for sol in dict_ex['soluciones']:
            definicion_oculta = (orac.sustituir_sustantivo(nltk.word_tokenize(sol['definicion']), sol['palabra']))
            item = ItemEjercicioSustantivos(sol['palabra'], None, sol['definicion'], definicion_oculta)
            items.append(item)
        ret = EjercicioSustantivos(dict_ex['texto'], items)

    elif dict_ex['tipo'] == 'use_en':
        for opcion in dict_ex['opciones']:
            item = ItemEjercicioUseEn(opcion['solucion'], opcion['variantes'], opcion['referencia'])
            items.append(item)
        ejercicio = {
        'texto' : dict_ex['texto'],
        'items' : items
        }
        ret = EjercicioUseEn(dict_ex['texto_original'], ejercicio)

    return ret
