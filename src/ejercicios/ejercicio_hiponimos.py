import procesamientos.oraciones as orac
import procesamientos.hiponimos as hip
from recursos.categorias import Categorias
from procesamientos.sustantivos import es_sustantivo
from procesamientos.procesamiento import obtener_palabras, es_adjetivo
import nltk
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
        filtro = lambda x: es_sustantivo(x) or es_adjetivo(x)
        lista_palabras = obtener_palabras(filtro, texto)

        lista_palabras = list({ each['token'] : each for each in lista_palabras }.values())
        for palabra in lista_palabras:
            palabra_token = lemma(palabra['token'])
            categorias = Categorias().listar_categorias()
            palabra_categoria = None
            for categoria in categorias:
                categoria_synset_id = categoria['synset_id']
                es_hiponimo = hip.es_hiponimo(palabra_token, categoria_synset_id)
                if es_hiponimo:
                    palabra_categoria = categoria['nombre']
            if palabra_categoria:
                # Evitar palabras duplicadas
                if not any(obj.palabra == palabra_token for obj in items_ejercicio):
                    item = ItemEjercicioHiponimos(palabra_token, palabra_categoria)
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
