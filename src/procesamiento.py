import nltk

# Toma un texto taggeado y devuelve una lista que contiene "token, pos_tags, posicion_palabra"
def parse_pos_tags(pos_tags):
    return [{ 'token':t, 'pos_tag':p, 'posicion':i } for i,(t,p) in enumerate(pos_tags)]

# Devuelve las palabras con su pos tag y posición en el texto ingresado
# Retorna [{'token':token, 'pos_tag':pos_tag, 'posicion':posicion}]
def obtener_palabras(filtro, tokens):
    pos_tags = nltk.pos_tag(tokens)
    pos_tags_con_posiciones = parse_pos_tags(pos_tags)
    palabras = list(filter(filtro, pos_tags_con_posiciones))
    return palabras

def serialize_ojectid(lista):
    results = []
    for document in lista:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results

def flatten(lista):
    lista_plana = []
    for sublista in lista:
        if isinstance(sublista, list):
            for item in sublista:
                lista_plana.append(item)
        else:
            lista_plana.append(sublista)
    return lista_plana
