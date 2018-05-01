import json

def procesar_diccionario(path):
    json_entrada = json.load(open(path))
    json_salida = []
    for entrada in json_entrada['entry_list']:
        definiciones = []
        for part_of_speech in entrada['part_of_speech_list']:
            if part_of_speech['name_list'][0] == 'phrase': continue
            for sense in part_of_speech['sense_list']:
                if 'definition' not in sense: continue
                definicion = {
                    'definicion': sense['definition'],
                    'tipo' : part_of_speech['name_list'][0],
                }
                if 'example_list' in sense:
                    definicion['ejemplo'] = sense['example_list'][0]
                if 'spanish' in sense and 'translation_list' in sense['spanish']:
                    definicion['traducciones'] = sense['spanish']['translation_list']
                definiciones.append(definicion)
        salida = {
            'palabra': entrada['headword_ne'],
            'definiciones': definiciones
        }
        if len(salida['definiciones']) > 0: json_salida.append(salida)
