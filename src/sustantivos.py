import nltk
from procesamiento import obtener_palabras
from diccionario import Diccionario
from pattern.en import lemma
from nltk.wsd import lesk

dicc = Diccionario()

# Evalua segun si el pos_tag del token es un sustantivo
def es_sustantivo(token_pos_tag):
    pos_tag = token_pos_tag['pos_tag']
    sustantivo_pos_tag = 'NN'
    if (pos_tag[0:2] == sustantivo_pos_tag):
        return True
    return False

# Retorna si la palabra pasada por parametro se encuentra en el diccionario
def esta_diccionario(sustantivo):
    definicion = encontrar_definicion(sustantivo)
    if definicion:
        return True
    return False

# Devuelve la definicion encontrada asociada a un sustantivo
# Si no la encuntra devuelve NoneType
def encontrar_definicion(sustantivo):    
    definicion = dicc.buscar_definicion(sustantivo)
    if definicion:
        return definicion
    else:
        lema = lemma(sustantivo)
        return dicc.buscar_definicion(lema)


# Devuelve las palabras de un texto tokenizado que son sustantivos y ademas pertenecen al diccionario.
def obtener_sustantivos(tokens):
    return obtener_palabras(lambda x: es_sustantivo(x) and esta_diccionario(x['token']), tokens)

def filtrar_sustantivos(tokens, cant_sustantivos):
    return tokens[:cant_sustantivos]

# Devuelve la definicion de un sustantivo. 
# En caso de haber mas de una busca segun el sentido de la palabra en el texto tokenizado.
def obtener_mejor_definicion(tokens, sustantivo):
    definiciones = encontrar_definicion(sustantivo)['definiciones']
    sustantivos_def = list(filter(lambda x: x['tipo'] == 'noun', definiciones))
    if len(sustantivos_def) == 1:
        return definiciones[0]['definicion']
    else:
        synset = lesk(tokens, sustantivo, 'n')
        return synset.definition()
