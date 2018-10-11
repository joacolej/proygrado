import kenlm
import nltk

# model_path = '../../wiki.klm'
model_path = '../../language-model/modelos/wiki-min.klm'
model = kenlm.LanguageModel(model_path)

def score_texto(texto):
    texto_procesado = ' '.join(nltk.word_tokenize(texto)).lower()
    return model.score(texto_procesado)
