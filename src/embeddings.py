import itertools
from gensim import Word2Vec

# fitting to the corpus and adding standard dictionary to the object

class Embeddings:
    def __init__(self, sentences = None, model_path = None):
        if not sentences is None:
            self.model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
        if not model_sentences is None:
            self.model = Word2Vec.load(model_path)

    def guardar_modelo(self, path):
        self.model.save(path)

    def obtener_palabras_similares(self, word):
        model.wv.most_similar(positive=word)
