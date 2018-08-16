import kenlm

model_path = '../recursos/modelos/wiki-simple.klm'
# model_path = '../../language-model/modelos/wiki.klm'
model = kenlm.LanguageModel(model_path)

def score_texto(texto):
    return model.score(texto)
