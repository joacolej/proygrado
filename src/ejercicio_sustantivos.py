import nltk
import sustantivos as st
import oraciones as orac

# Ejercicio para matchear sustantivos con sus definiciones
def ejercicio_sustantivos(nombre_texto):
    archivo = open(nombre_texto, 'r+')
    data = archivo.read()
    ejercicios = procesar_ejercicio_sustantivos(data)
    return ejercicios

# Retorna los sustantivos seleccinados con su correspondiente definicion
def procesar_ejercicio_sustantivos(texto):
    tokens = nltk.word_tokenize(texto)
    lista_sustantivos = st.obtener_sustantivos(tokens)
    palabras, definiciones, soluciones = ([] for i in range(3))
    for sustantivo in lista_sustantivos:
        palabras.append(sustantivo['token'])
        definicion = st.obtener_mejor_definicion(tokens, sustantivo['token'])
        definicion_tokens = nltk.word_tokenize(definicion)
        definiciones.append(orac.sustituir_sustantivo(definicion_tokens, sustantivo['token']))
        solucion = {
            'palabra': sustantivo['token'], 'definicion': definicion 
        }
        soluciones.append(solucion)
    ejercicio = {
        'palabras': palabras,
        'definiciones': definiciones,
        'soluciones': soluciones
    }
    return ejercicio
