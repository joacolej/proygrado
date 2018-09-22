import json
from lista_de_frecuencia import Frecuencia
from utils import abrir_json_file

# El vocabulario es la union de las palabras mas frecuentes mas la lista de palabras movers
class Vocabulario:
    def __init__(self):
        frec = Frecuencia()
        with open('../recursos/lista_palabras_movers.json') as data_file:
            movers = json.load(data_file)
        lista_movers = movers['verbos'] + movers['determinantes'] + movers['preposiciones'] + movers['adverbios'] + movers['conjunciones'] + movers['adjetivos'] + movers['pronombres'] + movers['sustantivos']
        palabras_frecuentes = frec.data['palabra'].tolist()[0:5000]
        self.vocabulario = set(lista_movers + palabras_frecuentes)

    def generar_txt(self):
        f = open('./recursos/vocabulario.txt','w')
        for palabra in self.vocabulario:
            f.write(palabra + '\n')
        f.close()
    
    def generar_json(self):
        data = { 'vocabulario': list(self.vocabulario) }
        with open('../recursos/vocabulario.json', 'w') as outfile:  
            json.dump(data, outfile)

    def pertenece(self, palabra):
        if palabra.lower() in self.vocabulario:
            return True
        return False
