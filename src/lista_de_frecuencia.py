import pandas as pd

class Frecuencia:
    def __init__:
        self.data = pd.read_csv('../recursos/frequency_wikimedia', sep=" ", header=None)
        self.data.columns = ['numero', 'palabra', 'frecuencia']
        self.data = data.drop(columns=['numero'])

    def obtener_frecuencia(palabra):
        if palabra in self.data['palabra'].tolist():
            elem = self.data.loc[self.data['palabra'] == palabra]['frecuencia']
            return elem.tolist()[0]
        else:
            return 0.0

    def obtener_mas_frecuente(lista_palabras):
        frecuencia_maxima = max([obtener_frecuencia(x) for x in lista_palabras])
        for palabra in lista_palabras:
            if obtener_frecuencia(palabra) == frecuencia_maxima:
                return palabra