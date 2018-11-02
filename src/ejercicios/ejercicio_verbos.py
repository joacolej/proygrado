import nltk
import procesamientos.verbos as vb
import procesamientos.oraciones as orac
from pattern.en import lexeme

def ejercicio_verbos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_verbos(data)
    return ejercicios

def procesar_ejercicio_verbos(texto):
    parrafos = texto.split('\n')
    posicion_inicial = 0
    cant_verbos = 0
    texto_ejercicio = []
    opciones = []
    for parrafo in parrafos:
        tokens = nltk.word_tokenize(parrafo)
        lista_verbos = vb.obtener_verbos(parrafo)
        for idx, verbo in enumerate(lista_verbos):
            conjugaciones = lexeme(verbo['token'])
            conjugaciones = vb.filtrar_conjugaciones(verbo, conjugaciones)
            opcion = {
                'posicion': verbo['posicion'] + posicion_inicial,
                'variantes': conjugaciones,
                'solucion': verbo['token'],
                'referencia': '(' + str(idx + cant_verbos) + ')'
            }
            opciones.append(opcion)
        texto_ejercicio.append(orac.sustituir_verbos(tokens, lista_verbos, cant_verbos))
        posicion_inicial = posicion_inicial + len(tokens)
        cant_verbos = cant_verbos + len(lista_verbos)
    ejercicio = {
        'texto': '\n'.join(texto_ejercicio),
        'opciones': opciones,
        'tipo': 'verbos'
    }
    return ejercicio