import procesamientos.sustantivos as st
import procesamientos.oraciones as orac
import procesamientos.hiponimos as hip
from recursos.categorias import Categorias
import nltk
import random
from pattern.en import lemma

class EjercicioHiponimos():
    def __init__(self, parrafo):
        self.parrafo = parrafo
        self.items = self.procesar_ejercicio_hiponimos(parrafo)

    def procesar_ejercicio_hiponimos(self, texto):
        items_ejercicio = []
        lista_sustantivos = st.obtener_sustantivos(texto)
        lista_sustantivos = list({ each['token'] : each for each in lista_sustantivos }.values())
        for sustantivo in lista_sustantivos:
            palabra = lemma(sustantivo['token'])
            categorias = Categorias().listar_categorias()
            palabra_categoria = None
            for categoria in categorias:
                categoria_synset_id = categoria['synset_id']
                es_hiponimo = hip.es_hiponimo(palabra, categoria_synset_id)
                if es_hiponimo:
                    palabra_categoria = categoria['nombre']
            if palabra_categoria:
                data = { 'palabra': palabra, 'categoria': palabra_categoria}
                items_ejercicio.append(data)
        return items_ejercicio
