import pymongo
from bson.objectid import ObjectId
import datetime

# Singleton Textos
class Textos:
    class __Textos:
        def __init__(self):
            puerto = 27017
            client = pymongo.MongoClient('localhost', puerto)
            db = client.textos_db
            self.textos = db.textos

    instance = None

    def __init__(self):
        if not Textos.instance:
            Textos.instance = Textos.__Textos()
        else:
            Textos.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def agregar_texto(self, texto):
        # Prevenir de agregar textos duplicados
        if not self.existe_texto(texto):
            data_texto = {
                'texto': texto,
                'date': datetime.datetime.utcnow()
            }
            self.textos.insert_one(data_texto)

    def remover_texto(self, id):
        self.textos.delete_one({ '_id': ObjectId(id) })

    def listar_textos(self):
        return self.textos.find()

    def buscar_texto(self, id):
        return self.textos.find_one({ '_id': ObjectId(id) })

    def existe_texto(self, texto):
        return bool(self.textos.find_one({ 'texto': texto }))
