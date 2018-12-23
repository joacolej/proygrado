import pymongo
from bson.objectid import ObjectId
import datetime

class Ejercicio:
    class __Ejercicio:
        def __init__(self):
            puerto = 27017
            client = pymongo.MongoClient('localhost', puerto)
            db = client.ejercicio_db
            self.ejercicios = db.ejercicios

    instance = None

    def __init__(self):
        if not Ejercicio.instance:
            Ejercicio.instance = Ejercicio.__Ejercicio()
        else:
            Ejercicio.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def agregar_ejercicio(self, ejercicio):
        ejercicio['date'] = datetime.datetime.utcnow()
        if self.ejercicios.count() > 0:
            ejercicios_list = list(self.listar_ejercicios())
            ejercicios_list.reverse()
            next_numero = ejercicios_list[0]['numero'] + 1
            ejercicio['numero'] = next_numero
        else:
            ejercicio['numero'] = 1
        ejercicio_id = self.ejercicios.insert_one(ejercicio).inserted_id
        return self.buscar_ejercicio(ejercicio_id)

    def remover_ejercicio(self, id):
        self.ejercicios.delete_one({ '_id': ObjectId(id) })

    def buscar_ejercicio(self, id):
        return self.ejercicios.find_one({ '_id': ObjectId(id) })

    def listar_ejercicios(self):
        return self.ejercicios.find()

    def buscar_ultimo_ejercicio(self):
        return self.ejercicios.find_one()
