from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask.json import jsonify
from ejercicio_verbos import procesar_ejercicio_verbos
from ejercicio_sustantivos import procesar_ejercicio_sustantivos
from procesamiento import serialize_ojectid
from ejercicio import Ejercicio
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
        ret = procesar_ejercicio_sustantivos(texto)
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
        ejercicios = serialize_ojectid(lista)
        return jsonify(ejercicios)

api.add_resource(Verbos, '/ejercicio-verbos', methods=['POST']) # Route_1
api.add_resource(Sustantivos, '/ejercicio-sustantivos', methods=['POST']) # Route_2
api.add_resource(EjercicioArmado, '/ejercicios', methods=['POST', 'GET']) # Route_3

if __name__ == '__main__':
    app.run(port='3000', threaded=True, host='0.0.0.0')
