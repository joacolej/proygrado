import nltk
import procesamientos.verbos as vb
import procesamientos.oraciones as orac
import itertools
from pattern.en import lexeme
from constantes import CARACTER_BLANCO

class ItemEjercicioVerbos():

    def __init__(self, solucion, variantes, referencia, posicion, tiempo_verbal):
        self.solucion = solucion
        self.variantes = variantes
        self.referencia = referencia
        self.posicion = posicion
        self.tiempo_verbal = tiempo_verbal

class EjercicioVerbos():
    def __init__(self, parrafo, ejercicio = None):
        self.referencia = itertools.count()
        self.parrafo = parrafo
        self.numeros_siguientes = []
        if not ejercicio:
            ejercicio = self.procesar_ejercicio_verbos(parrafo)
        self.parrafo_sustituido = ejercicio['texto']
        self.items = ejercicio['items']

    def procesar_ejercicio_verbos(self, texto):
        parrafos = texto.split('\n')
        posicion_inicial = 0
        cant_verbos = 0
        texto_ejercicio = []
        items_ejercicio = []
        for parrafo in parrafos:
            tokens = nltk.word_tokenize(parrafo)
            lista_verbos = vb.obtener_verbos(parrafo)
            for idx, verbo in enumerate(lista_verbos):
                conjugaciones = lexeme(verbo['token'])
                conjugaciones = vb.filtrar_conjugaciones(verbo, conjugaciones)
                tiempo_verbal = vb.obtener_tiempo(verbo['pos_tag'])
                item = ItemEjercicioVerbos(verbo['token'], conjugaciones, str(idx + cant_verbos), verbo['posicion'] + posicion_inicial, tiempo_verbal)
                items_ejercicio.append(item)
            texto_ejercicio.append(orac.sustituir_verbos(tokens, lista_verbos, cant_verbos))
            posicion_inicial = posicion_inicial + len(tokens)
            cant_verbos = cant_verbos + len(lista_verbos)
        ejercicio = {
            'texto': '\n'.join(texto_ejercicio),
            'items': items_ejercicio
        }
        return ejercicio

    def eliminar_item(self, referencia):
        dicc = { '(': '', ')': '' }
        referencia = orac.sustituir_todos(referencia, dicc)
        item = [x for x in self.items if x.referencia == referencia][0]
        print(item.solucion)
        print(self.parrafo_sustituido)
        dicc = { '(' + referencia + ') ' + CARACTER_BLANCO + '(' + item.tiempo_verbal + ')': item.solucion }
        for i in range(int(item.referencia), len(self.items) - 1):
            dicc['(' + str(i + 1) + ') '] = '(' + str(i) + ') '
            self.items[i+1].referencia = str(i)
        self.parrafo_sustituido = orac.sustituir_todos(self.parrafo_sustituido, dicc)
        print(self.parrafo_sustituido)
        self.items.remove(item)
        self.numeros_siguientes.append(referencia)

    def exportar_ejercicio(self):
        opciones = []
        for item in self.items:
            opcion = {
                'posicion': item.posicion,
                'variantes': item.variantes,
                'solucion': item.solucion,
                'referencia': '(' + str(item.referencia) + ')',
                'tiempo_verbal': item.tiempo_verbal
            }
            opciones.append(opcion)
        ejercicio = {
        'texto': self.parrafo_sustituido,
        'texto_original': self.parrafo,
        'opciones': opciones,
        'tipo': 'verbos'
        }
        return ejercicio
