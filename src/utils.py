import json

# Importa y lee un archivo del tipo json
def abrir_json_file(ruta_texto):
    with open(ruta_texto) as data_file:
        data = json.load(data_file)
    return data
