import pandas as pd

class Frecuencia:
    def __init__(self):
        self.data = pd.read_csv('../../recursos/frequency_wikimedia', sep=" ", header=None)
        self.data.columns = ['numero', 'palabra', 'frecuencia']
        self.data = self.data.drop(columns=['numero'])

    def obtener_frecuencia(self, palabra):
        if palabra in self.data['palabra'].tolist():
            elem = self.data.loc[self.data['palabra'] == palabra]['frecuencia']
            return elem.tolist()[0]
        else:
            return 0.0

    def obtener_mas_frecuente(self, lista_palabras):
        frecuencia_maxima = max([obtener_frecuencia(x) for x in lista_palabras])
        for palabra in lista_palabras:
            if self.obtener_frecuencia(palabra) == frecuencia_maxima:
                return palabra

    def ordenar_por_frecuencia(self, lista_palabras):
        return sorted(lista_palabras, key=self.obtener_frecuencia)
