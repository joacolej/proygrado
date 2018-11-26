import procesamientos.palabras_use_en
import procesamientos.sustantivos as st
import procesamientos.oraciones as orac
import nltk
import random


class ItemEjercicioSustantivos():

    def __init__(self, palabra, posicion, definicion, definicion_oculta):
        self.palabra = palabra
        self.posicion = posicion
        self.definicion = definicion
        self.definicion_oculta = definicion_oculta

class EjercicioSustantivos():

    def __init__(self, parrafo):
        self.parrafo = parrafo
        self.items = self.procesar_ejercicio_sustantivos(parrafo)

    def procesar_ejercicio_sustantivos(self, texto):
        items_ejercicio = []
        tokens = nltk.word_tokenize(texto)
        lista_sustantivos = st.obtener_sustantivos(texto)
        lista_sustantivos = list({ each['token'] : each for each in lista_sustantivos }.values())
        for sustantivo in lista_sustantivos:
            palabra = sustantivo['token']
            posicion = sustantivo['posicion']
            definicion = st.obtener_mejor_definicion(tokens, palabra)
            definicion_tokens = nltk.word_tokenize(definicion)
            definicion_oculta = (orac.sustituir_sustantivo(definicion_tokens, sustantivo['token']))
            item = ItemEjercicioSustantivos(palabra, posicion, definicion, definicion_oculta)
            items_ejercicio.append(item)
        return items_ejercicio

    def modificar_ejercicio(self, dict):
        for item in self.items:
            if item.palabra == dict['palabra']:
                mod = item

        for key in dict:
            if key == 'definicion':
                mod.definicion = dict['definicion']
                mod.definicion_oculta = (orac.sustituir_sustantivo(nltk.word_tokenize(mod.definicion), mod.palabra))


    def exportar_ejercicio(self):
        palabras = []
        definiciones = []
        soluciones = []
        for item in self.items:
            palabras.append(item.palabra)
            definiciones.append(item.definicion)
            solucion = {
                'palabra': item.palabra, 'definicion': item.definicion
            }
            soluciones.append(solucion)
        random.shuffle(palabras)
        random.shuffle(definiciones)
        ejercicio = {
            'palabras': palabras,
            'definiciones': definiciones,
            'soluciones': soluciones,
            'tipo': 'sustantivos'
        }
        return ejercicio

    def eliminar_item(self, palabra):
        self.items = list(filter(lambda x: x.palabra != palabra, self.items))

    def agregar_item(self, palabra, definicion = None, posicion = -1):
        if not definicion:
            definiciones = st.encontrar_definicion(palabra)
            definicion = definiciones[0]['definicion']
            definicion_tokens = nltk.word_tokenize(definicion)
            defi = (orac.sustituir_sustantivo(definicion_tokens, palabra))
            item = ItemEjercicioSustantivos(palabra, posicion, defi)
        else:
            item = ItemEjercicioSustantivos(palabra, posicion, definicion)
        self.items.append(item)
