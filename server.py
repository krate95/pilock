#!flask/bin/python
from flask import Flask, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

class Cerradura(Resource):
    def got(self):
        return jsonify()

api.add_resource(Cerradura, '/cerradura')

if __name__ == '__main__':
    app.run(host='0.0.0.0')