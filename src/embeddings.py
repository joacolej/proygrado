import itertools
from gensim.models import Word2Vec
from gensim.utils import to_utf8

# fitting to the corpus and adding standard dictionary to the object

class Embeddings:
    def __init__(self, model_path = None):
        # if not sentences is None:
        #     self.model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
        # if not model_sentences is None:
        self.model = Word2Vec.load(model_path)

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
