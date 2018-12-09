import nltk
from random import shuffle
import procesamientos.sustantivos as st
import procesamientos.oraciones as orac
import procesamientos.palabras_use_en as use_en
import itertools
from procesamientos.procesamiento import parse_pos_tags
from constantes import CARACTER_BLANCO

class ItemEjercicioUseEn():

    def __init__(self, solucion, variantes, referencia):
        self.solucion = solucion
        self.variantes = variantes
        self.referencia = referencia

class EjercicioUseEn():
    def __init__(self, parrafo, ejercicio = None):
        self.referencia = itertools.count()
        self.parrafo = parrafo
        self.numeros_siguientes = []
        if not ejercicio:
            ejercicio = self.procesar_use_en(parrafo)
        self.parrafo_sustituido = ejercicio['texto']
        self.items = ejercicio['items']

# Retorna los sustantivos seleccionados con su correspondiente definicion
    def procesar_use_en(self, texto):
        items_ejercicio = []
        texto_ejercicio = []
        oraciones = orac.separar_oraciones(texto)
        palabras_usadas = []
        for oracion in oraciones:
            tokens = nltk.word_tokenize(oracion)
            lista_palabras = use_en.seleccionar_palabras(oracion, palabras_usadas=palabras_usadas)
            if len(lista_palabras) == 0:
                texto_ejercicio.append(oracion)
            for palabra in lista_palabras:
                referencia_actual = next(self.referencia)
                variantes = use_en.filtro_categoria_movers(palabra)
                variantes = use_en.filtro_similaridad(palabra['token'], variantes)
                variantes_finales = use_en.filtrar_palabras(palabra['token'], variantes, oracion)
                if not palabra['token'][0].islower():
                    variantes_finales = [x.capitalize() for x in variantes_finales]
                variantes_finales.append(palabra['token'])
                shuffle(variantes_finales)
                item = ItemEjercicioUseEn(palabra['token'], variantes_finales, referencia_actual)
                palabras_usadas.append(palabra['token'])
                texto_ejercicio.append(orac.sustituir_palabra(oracion, palabra['token'], referencia_actual))
                items_ejercicio.append(item)
        ejercicio = {
            'texto': ' '.join(texto_ejercicio),
            'items': items_ejercicio,
        }
        return ejercicio

    def eliminar_item(self, referencia):
        dicc = { '(': '', ')': '' }
        referencia = orac.sustituir_todos(referencia, dicc)
        item = [x for x in self.items if x.referencia == referencia][0]
        print(item.solucion)
        print(self.parrafo_sustituido)
        dicc = { '(' + referencia + ') ' + CARACTER_BLANCO: item.solucion }
        for i in range(int(item.referencia), len(self.items) - 1):
            dicc['(' + str(i + 1) + ') '] = '(' + str(i) + ') '
            self.items[i+1].referencia = str(i)
        self.parrafo_sustituido = orac.sustituir_todos(self.parrafo_sustituido, dicc)
        print(self.parrafo_sustituido)
        self.items.remove(item)
        self.numeros_siguientes.append(referencia)

    def agregar_item(self, solucion, variantes):
        if self.numeros_siguientes:
            referencia = self.numeros_siguientes.pop()
        else:
            referencia = next(self.referencia)
        variantes_finales = variantes + [solucion]
        shuffle(variantes_finales)
        item = ItemEjercicioUseEn(solucion, variantes_finales, referencia)
        self.parrafo_sustituido = orac.sustituir_palabra(self.parrafo_sustituido, solucion, referencia)
        self.items.append(item)

    def exportar_ejercicio(self):
        opciones = []
        for item in self.items:
            opcion = {
                'variantes': item.variantes,
                'solucion': item.solucion,
                'referencia': '(' + str(item.referencia) + ')'
            }
            opciones.append(opcion)
        ejercicio = {
        'texto_original': self.parrafo,
        'texto': self.parrafo_sustituido,
        'opciones': opciones,
        'tipo': 'use_en'
        }
        return ejercicio

    # def procesar_use_en_old(self, texto):
    #     items_ejercicio = []
    #     texto_ejercicio = []
    #     oraciones = orac.separar_oraciones(texto)
    #     referencia = itertools.count()
    #     palabras_usadas = []
    #     for oracion in oraciones:
    #         tokens = nltk.word_tokenize(oracion)
    #         lista_palabras = use_en.seleccionar_palabras(oracion, palabras_usadas=palabras_usadas)
    #         for palabra in lista_palabras:
    #             referencia_actual = next(referencia)
    #             variantes = use_en.filtro_categoria_movers(palabra)
    #             variantes = use_en.filtro_similaridad(palabra['token'], variantes)
    #             variantes_finales = use_en.filtrar_palabras(palabra['token'], variantes, oracion)
    #             variantes_finales.append(palabra['token'])
    #             shuffle(variantes_finales)
    #             opcion = {
    #                 'variantes': variantes_finales,
    #                 'solucion': palabra['token'],
    #                 'referencia': '(' + str(referencia_actual) + ')'
    #             }
    #             palabras_usadas.append(palabra['token'])
    #             texto_ejercicio.append(orac.sustituir_palabra(oracion, palabra['token'], referencia_actual))
    #             opciones.append(opcion)
    #     ejercicio = {
    #         'texto': '\n'.join(texto_ejercicio),
    #         'opciones': opciones,
    #         'tipo': 'use_of_en'
    #     }
    #     return ejercicio
