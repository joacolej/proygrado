import itertools
from gensim.models import Word2Vec
from gensim.utils import to_utf8
import os

MODEL_PATH=os.getenv("EMBEDDINGS_MODEL_PATH")
model = Word2Vec.load(MODEL_PATH)

class Embeddings:
    def __init__(self):
        self.model = model

    def guardar_modelo(self, path):
        self.model.save(path)

    def obtener_palabras_similares(self, word):
        most_similar = self.model.wv.most_similar(positive=word)
        # Palabras to uft8
        return list(map(lambda (palabra, prob): (to_utf8(palabra), prob), most_similar))

    def similarity(self, palabra1, palabra2):
        try:
            return self.model.wv.similarity(palabra1, palabra2)
        except:
            return 0
