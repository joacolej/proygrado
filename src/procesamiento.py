import nltk

# Toma un texto taggeado y devuelve una lista que contiene "token, pos_tags, posicion_palabra"
def parse_pos_tags(pos_tags):
    return [{ 'token':t, 'pos_tag':p, 'posicion':i } for i,(t,p) in enumerate(pos_tags)]

# Devuelve los verbos con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_palabras(filtro, tokens):
    pos_tags = nltk.pos_tag(tokens)
    pos_tags_con_posiciones = parse_pos_tags(pos_tags)
    verbos = list(filter(filtro, pos_tags_con_posiciones))
    return verbos
