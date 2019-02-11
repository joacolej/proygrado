import kenlm
import nltk
import os

MODEL_PATH = os.getenv("LANGUAGE_MODEL_PATH")
model = kenlm.LanguageModel(MODEL_PATH)

def score_texto(texto):
    texto_procesado = ' '.join(nltk.word_tokenize(texto)).lower()
    return model.score(texto_procesado)
