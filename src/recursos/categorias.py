import pymongo

# Singleton Categorias
class Categorias:
    class __Categorias:
        def __init__(self):
            puerto = 27017
            client = pymongo.MongoClient('localhost', puerto)
            db = client.categorias_db
            self.categorias = db.categorias
            self.categorias.create_index('nombre', unique=True)

    instance = None

    def __init__(self):
        if not Categorias.instance:
            Categorias.instance = Categorias.__Categorias()
        else:
            Categorias.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def agregar_categoria(self, nombre, synset_id):
        categoria = { 'nombre': nombre, 'synset_id': synset_id }
        self.categorias.insert_one(categoria)

    def remover_categoria(self, nombre):
        self.categoria.delete_one({ 'nombre': nombre })

    def listar_categorias(self):
        return self.categorias.find()

    def buscar_categoria(self, nombre):
        return self.categorias.find_one({ 'nombre': nombre})

    def cargar_categorias(self, lista_categorias):
        self.categorias.insert_many(lista_categorias)
