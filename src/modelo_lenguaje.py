import kenlm

def score_texto(texto):
    model_path = '../recursos/modelos/wiki-simple.klm'    
    model = kenlm.LanguageModel(model_path)
    return model.score(texto)
