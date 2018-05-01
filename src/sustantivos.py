import nltk

# Evalua segun si el pos_tag del token es un sustantivo
def es_sustantivo(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    sustantivo_pos_tag = 'NN'
    if (pos_tag[0:2] == sustantivo_pos_tag):
        return True
    return False

def obtener_sustantivos(tokens):
    return obtener_palabras(es_sustantivo, tokens)

def filtrar_sustantivos(tokens, cant_sustantivos):
    return tokens[:cant_sustantivos]
