from dotenv import load_dotenv
# Load environment variables
load_dotenv('.env')

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask.json import jsonify
from ejercicios.ejercicio_verbos import EjercicioVerbos
from ejercicios.ejercicio_sustantivos import EjercicioSustantivos
from ejercicios.ejercicio_use_en import EjercicioUseEn
from ejercicios.ejercicio_hiponimos import EjercicioHiponimos
from procesamientos.procesamiento import serialize_array_objectId, serialize_objectId
from ejercicio import Ejercicio
from recursos.diccionario import Diccionario
from recursos.vocabulario import Vocabulario
from recursos.textos import Textos
from ejercicios.importar import importar_ejercicio, importar_st_modificado
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

def pre_procesamiento_ejercicio(request):
    content = request.json
    texto = content.get('texto')
    recordar_texto = content.get('recordar_texto')
    if recordar_texto:
        Textos().agregar_texto(texto)
    return texto

class Verbos(Resource):
    def post(self):
        texto = pre_procesamiento_ejercicio(request)
        ejercicio_verbos = EjercicioVerbos(texto)
        ret = ejercicio_verbos.exportar_ejercicio()
        return jsonify(ret)

class Sustantivos(Resource):
    def post(self):
        texto = pre_procesamiento_ejercicio(request)
        ejercicio_sustantivos = EjercicioSustantivos(texto)
        ret = ejercicio_sustantivos.exportar_ejercicio()
        return jsonify(ret)

    def put(self):
        content = request.json
        ejercicio_ex = content.get('ejercicio')
        referencia = content.get('referencia')
        definicion = content.get('definicion')
        ejercicio = importar_st_modificado(ejercicio_ex, referencia, definicion)
        ejercicio_actualizado = ejercicio.exportar_ejercicio()
        return jsonify(ejercicio_actualizado)

class Hiponimos(Resource):
    def post(self):
        content = request.json
        texto = content.get('texto')
        ejercicio_hiponimos = EjercicioHiponimos(texto)
        ret = ejercicio_hiponimos.exportar_ejercicio()
        return jsonify(ret)

class UseOfEnglish(Resource):
    def post(self):
        texto = pre_procesamiento_ejercicio(request)
        ejercicio_use_en = EjercicioUseEn(texto)
        ret = ejercicio_use_en.exportar_ejercicio()
        return jsonify(ret)

class EliminarReferencias(Resource):
    def put(self):
        content = request.json
        ejercicio_ex = content.get('ejercicio')
        texto_referencia = content.get('referencia')
        ejercicio = importar_ejercicio(ejercicio_ex)
        ejercicio.eliminar_item(texto_referencia)
        ejercicio_actualizado = ejercicio.exportar_ejercicio()
        return jsonify(ejercicio_actualizado)

class EjercicioArmado(Resource):
    def post(self):
        ej = Ejercicio()
        content = request.json
        ejercicio = content.get('ejercicio')
        ejercicio_ex = ej.agregar_ejercicio(ejercicio)
        resp = jsonify(serialize_objectId(ejercicio_ex))
        return resp

    def get(self):
        ej = Ejercicio()
        lista = ej.ejercicios.find()
        ejercicios = serialize_array_objectId(lista)
        return jsonify(ejercicios)

class PalabrasDefiniciones(Resource):
    def get(self):
        dic = Diccionario()
        lista = dic.listar_definiciones()
        definiciones = serialize_array_objectId(lista)
        palabras = map(lambda x: x['palabra'], definiciones)
        return jsonify(palabras)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('definicion')
        parser.add_argument('palabra')
        args = parser.parse_args()
        palabra = args['palabra']
        definicion = args['definicion']
        Diccionario().agregar_definicion(palabra, definicion)
        return palabra, 201

class Definicion(Resource):
    def get(self, palabra):
        dic = Diccionario()
        try:
            definicion = serialize_objectId(dic.buscar_definicion(palabra))
            return jsonify(definicion)
        except:
            return 'definicion no encontrada', 404

class Palabras(Resource):
    def get(self):
        vocabulario = map(lambda x: x['palabra'], list(Vocabulario().listar_vocabulario()))
        return jsonify(vocabulario)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('palabra')
        args = parser.parse_args()
        palabra = args['palabra']
        Vocabulario().agregar_palabra(palabra)
        return palabra, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('palabra')
        args = parser.parse_args()
        palabra = args['palabra']
        Vocabulario().remover_palabra(palabra)
        return palabra, 200

class TextosGuardados(Resource):
    def get(self):
        textos = map(lambda x: {
            'date': x['date'].strftime("%Y-%m-%d %H:%M:%S"),
            'texto': x['texto'],
            'id': x['_id']
        }, serialize_array_objectId(list(Textos().listar_textos())))
        return jsonify(textos)

api.add_resource(Verbos, '/ejercicio-verbos', methods=['POST']) # Route_1
api.add_resource(Sustantivos, '/ejercicio-sustantivos', methods=['POST', 'PUT']) # Route_2
api.add_resource(UseOfEnglish, '/ejercicio-use-of-en', methods=['POST']) # Route_3
api.add_resource(EliminarReferencias, '/eliminar-referencia', methods=['PUT']) # Route_4
api.add_resource(Hiponimos, '/ejercicio-hiponimos', methods=['POST']) # Route_5
api.add_resource(EjercicioArmado, '/ejercicios', methods=['POST', 'GET']) # Route_6
api.add_resource(PalabrasDefiniciones, '/palabras-definiciones', methods=['GET', 'POST']) # Route_7
api.add_resource(Definicion, '/definiciones/<palabra>', methods=['GET']) # Route_8
api.add_resource(Palabras, '/palabras', methods=['GET', 'POST', 'DELETE']) # Route_9
api.add_resource(TextosGuardados, '/textos', methods=['GET']) # Route_10

if __name__ == '__main__':
    app.run(port='3000', threaded=True, host='0.0.0.0')
