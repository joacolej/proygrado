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

