import json
from lista_de_frecuencia import Frecuencia
from utils import abrir_json_file
from pattern.en import PAST, PRESENT, INDICATIVE, PROGRESSIVE, conjugate
import pymongo

def conjugar_verbos(lista_verbos):
    lista_verbos_conjugados = []
    for verbo in lista_verbos:
        tercera_verb = conjugate(verbo, PRESENT, 3)
        past_verb = conjugate(verbo, PAST)
        past_participle_verb = conjugate(verbo, PAST, None, None, INDICATIVE, PROGRESSIVE)
        lista_verbos_conjugados.append(verbo)
        lista_verbos_conjugados.append(tercera_verb)
        lista_verbos_conjugados.append(past_verb)
        lista_verbos_conjugados.append(past_participle_verb)
    return lista_verbos_conjugados

# El vocabulario es la union de las palabras mas frecuentes mas la lista de palabras movers
class Vocabulario:
    class __Vocabulario:
        def __init__(self):
            puerto = 27017
            client = pymongo.MongoClient('localhost', puerto)
            db = client.vocabulario_db
            self.vocabulario = db.vocabulario
            self.vocabulario.create_index('palabra', unique=True)

    instance = None

    def __init__(self):
        if not Vocabulario.instance:
            Vocabulario.instance = Vocabulario.__Vocabulario()
        else:
            Vocabulario.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def generar_vocabulario(self):
        frec = Frecuencia()
        with open('../recursos/lista_palabras_movers.json') as data_file:
            movers = json.load(data_file)
        lista_movers = movers['verbos'] + movers['determinantes'] + movers['preposiciones'] + movers['adverbios'] + movers['conjunciones'] + movers['adjetivos'] + movers['pronombres'] + movers['sustantivos']
        verbos_conjugados = conjugar_verbos(movers['verbos'])
        palabras_frecuentes = frec.data['palabra'].tolist()[0:5000]
        return set(lista_movers + palabras_frecuentes + verbos_conjugados)

    def generar_txt(self):
        vocabulario = self.generar_vocabulario()
        f = open('./recursos/vocabulario.txt','w')
        for palabra in vocabulario:
            f.write(palabra + '\n')
        f.close()

    def generar_json(self):
        vocabulario = self.generar_vocabulario()
        data = { 'vocabulario': list(vocabulario) }
        with open('../recursos/vocabulario.json', 'w') as outfile:
            json.dump(data, outfile)

    def seed(self):
        vocabulario = list(self.generar_vocabulario())
        data = map(lambda x: { 'palabra': x }, vocabulario)
        self.cargar_vocabulario(data)

    def cargar_vocabulario(self, lista_vocabulario):
        self.vocabulario.insert_many(lista_vocabulario)

    def listar_vocabulario(self):
        return self.vocabulario.find()

    def agregar_palabra(self, palabra):
        self.vocabulario.insert_one({ 'palabra': palabra })

    def remover_palabra(self, palabra):
        self.vocabulario.delete_one({ 'palabra': palabra })

    def pertenece(self, palabra):
        vocabulario = map(lambda x: x['palabra'], list(self.listar_vocabulario()))
        if palabra.lower() in vocabulario:
            return True
        return False
