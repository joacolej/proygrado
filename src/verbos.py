import nltk

# Evalua según el pos tag si el token es un verbo
def es_verbo(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    verbo_pos_tag = 'VB'
    if (pos_tag[0:2] == verbo_pos_tag):
      return True
    return False

def es_gerundio(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    return pos_tag == 'VBG'

# Define el formato para devolver los verbos
def parse_pos_tags(pos_tags):
    return [{ 'token':t, 'pos_tag':p, 'posicion':i } for i,(t,p) in enumerate(pos_tags)]

# Devuelve los verbos con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_verbos(tokens):
    pos_tags = nltk.pos_tag(tokens)
    pos_tags_con_posiciones = parse_pos_tags(pos_tags)
    verbos = list(filter(lambda x: es_verbo(x) and not es_gerundio(x), pos_tags_con_posiciones))
    return verbos
