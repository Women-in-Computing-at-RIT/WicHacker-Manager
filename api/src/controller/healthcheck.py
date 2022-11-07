from flask_restful import Resource

class Healthcheck(Resource):
    PATH = '/'

    def get(self):
        return {"ping": "pong"}