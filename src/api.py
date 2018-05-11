#AQUI VA IR EL SERVIDOR :)

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask.json import jsonify
from ejercicio_verbos import procesar_ejercicio_verbos
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

#@app.route('/ejercicio-verbos', methods=['POST'])
class Verbos(Resource):
    def post(self):
        content = request.json
        texto = content.get('texto')
        ret = procesar_ejercicio_verbos(texto)
        return jsonify(ret)



api.add_resource(Verbos, '/ejercicio-verbos', methods=['POST']) # Route_1

if __name__ == '__main__':
    app.run(port='3000', threaded=True)
