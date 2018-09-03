import json

# Importa y lee un archivo del tipo json
def abrir_json_file(ruta_texto):
    with open(ruta_texto) as data_file:
        data = json.load(data_file)
    return data

def postag_a_synset(tag):
	if tag[0:2] == 'VB':
		return 'v'
	elif tag == 'NN':
		return 'n'
	elif tag == 'JJ':
		return 'a'
	elif tag == 'RB':
		return 'r'
	elif tag == 'RBR':
		return 's'

def obtener_categoria_palabras(pos_tag):
	if pos_tag[0:2] == 'VB':
		return 'verbos'
	elif pos_tag == 'NN' or pos_tag == 'NNS':
		return 'sustantivos'
	elif pos_tag[0:3] == 'NNP':
		return 'pronombres'
	elif pos_tag[0:2] == 'JJ':
		return 'adjetivos'
	elif pos_tag[0:2] == 'RB':
		return 'adverbios'
	elif pos_tag == 'CC':
		return 'conjunciones'
	elif pos_tag == 'DT':
		return 'determinantes'
	elif pos_tag == 'IN':
		return 'preposiciones'

