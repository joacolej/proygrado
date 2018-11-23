from nltk.corpus import wordnet

def es_hiponimo(palabra, categoria_id, cota = 20):
    synset_categoria = wordnet.synset(categoria_id)
    # Nos quedamos con el primer synset para v1
    synset = wordnet.synsets(palabra)[0]
    return check_hiponimo(synset, synset_categoria, cota)

def check_hiponimo(synset, synset_categoria, cota):
    hiponimos = synset.hypernyms()
    if not hiponimos:
        return False
    if cota == 0:
        return False
    else:
        es_hiponimo = False
        for hiponimo in hiponimos:
            if hiponimo == synset_categoria:
                es_hiponimo = True
            else:
                es_hiponimo = check_hiponimo(hiponimo, synset_categoria, cota - 1)
        return es_hiponimo

