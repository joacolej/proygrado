from dotenv import load_dotenv
# Load environment variables
load_dotenv('.env')

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask.json import jsonify
from ejercicios.ejercicio_verbos import procesar_ejercicio_verbos
from ejercicios.ejercicio_sustantivos import EjercicioSustantivos
from ejercicios.ejercicio_use_en import EjercicioUseEn
from procesamientos.procesamiento import serialize_array_objectId, serialize_objectId
from ejercicio import Ejercicio
from recursos.diccionario import Diccionario
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

class Verbos(Resource):
    def post(self):
        content = request.json
        texto = content.get('texto')
        ret = procesar_ejercicio_verbos(texto)
        return jsonify(ret)

class Sustantivos(Resource):
    def post(self):
        content = request.json
        texto = content.get('texto')
        ejercicio_sustantivos = EjercicioSustantivos(texto)
        ret = ejercicio_sustantivos.exportar_ejercicio()
        return jsonify(ret)

class UseOfEnglish(Resource):
    def post(self):
        content = request.json
        texto = content.get('texto')
        ejercicio_use_en = EjercicioUseEn(texto)
        ret = ejercicio_use_en.exportar_ejercicio()
        return jsonify(ret)

class EjercicioArmado(Resource):
    def post(self):
        ej = Ejercicio()
        content = request.json
        ejercicio = content.get('ejercicio')
        ej.agregar_ejercicio(ejercicio)
        response = {
            'message': 'Ejercicio creado'
        }
        resp = jsonify(response)
        resp.status_code = 201
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

class Definicion(Resource):
    def get(self, palabra):
        dic = Diccionario()
        try:
            definicion = serialize_objectId(dic.buscar_definicion(palabra))
            return jsonify(definicion)
        except:
            return 'definicion no encontrada', 404

api.add_resource(Verbos, '/ejercicio-verbos', methods=['POST']) # Route_1
api.add_resource(Sustantivos, '/ejercicio-sustantivos', methods=['POST']) # Route_2
api.add_resource(UseOfEnglish, '/ejercicio-use-of-en', methods=['POST']) # Route_3
api.add_resource(EjercicioArmado, '/ejercicios', methods=['POST', 'GET']) # Route_4
api.add_resource(PalabrasDefiniciones, '/palabras-definiciones', methods=['GET']) # Route_5
api.add_resource(Definicion, '/definiciones/<palabra>', methods=['GET']) # Route_6

if __name__ == '__main__':
    app.run(port='3000', threaded=True, host='0.0.0.0')
