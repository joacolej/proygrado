import pymongo

# Singleton Diccionario
class Diccionario:
    class __Diccionario:
        def __init__(self):
            puerto = 27017
            client = pymongo.MongoClient('localhost', puerto)
            db = client.diccionario_db
            self.definiciones = db.definiciones
            self.definiciones.create_index('palabra', unique=True)

    instance = None

    def __init__(self):
        if not Diccionario.instance:
            Diccionario.instance = Diccionario.__Diccionario()
        else:
            Diccionario.instance
    
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def agregar_definicion(self, definicion):
        self.definiciones.insert_one(definicion)

    def remover_definicion(self, palabra):
        self.definiciones.delete_one({ 'palabra': palabra })

    def listar_definiciones(self):
        return self.deficiones.find()

    def buscar_definicion(self, palabra):
        return self.definiciones.find_one({ 'palabra': palabra})

    def cargar_diccionario(self, lista_diccionario):
        self.definiciones.insert_many(lista_diccionario)
