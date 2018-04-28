import nltk
import json

# Importa y lee un archivo del tipo json
def abrir_json_file(ruta_texto):
    with open(ruta_texto) as data_file:
        data = json.load(data_file)
    data

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

def filtrar_verbos(lista_verbos):
    data = abrir_json_file('../recursos/lista_verbos_movers.json')
    for verbo in lista_verbos:
        if verbo['token'] in data['verbos']:
            lista_verbos.remove(verbo)
    lista_verbos
