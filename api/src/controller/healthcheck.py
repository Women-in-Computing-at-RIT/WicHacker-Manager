from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from utils.swagger import HEALTHCHECK_TAG


class Healthcheck(Resource):
    PATH = '/'

    @swagger.doc({
        'summary': "healthcheck",
        'tags': [HEALTHCHECK_TAG],
        'description': "endpoint to use for checking the health of the API",
        'responses': {
            '200': {
                'description': 'API is live'
            }
        }
    })
    def get(self):
        return {"ping": "pong"}