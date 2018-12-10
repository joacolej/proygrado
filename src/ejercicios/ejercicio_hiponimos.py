import procesamientos.sustantivos as st
import procesamientos.oraciones as orac
import procesamientos.hiponimos as hip
from recursos.categorias import Categorias
import nltk
import random
from pattern.en import lemma

class ItemEjercicioHiponimos():

    def __init__(self, palabra, categoria):
        self.palabra = palabra
        self.categoria = categoria

class EjercicioHiponimos():
    def __init__(self, parrafo, ejercicio = None):
        self.parrafo = parrafo
        self.numeros_siguientes = []
        if not ejercicio:
            self.items = self.procesar_ejercicio_hiponimos(parrafo)
        else:
            self.items = ejercicio

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
                item = ItemEjercicioHiponimos(palabra, palabra_categoria)
                items_ejercicio.append(item)
        return items_ejercicio

    def eliminar_item(self, palabra):
        self.items = list(filter(lambda x: x.palabra != palabra, self.items))

    def exportar_ejercicio(self):
        opciones = []
        for item in self.items:
            opcion = {
                'palabra': item.palabra,
                'categoria': item.categoria
            }
            opciones.append(opcion)
        categorias = [cat['nombre'] for cat in Categorias().listar_categorias()]
        ejercicio = {
            'texto_original': self.parrafo,
            'opciones': opciones,
            'categorias': categorias,
            'tipo': 'hiponimos'
        }
        return ejercicio
