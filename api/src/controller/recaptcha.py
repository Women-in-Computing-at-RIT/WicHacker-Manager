import logging

from flask_restful import Resource, reqparse
from flask import request
from flask_restful_swagger_2 import swagger, Schema

from data.recaptcha import getCaptchaResults
from utils.swagger import PERMISSIONS_TAG

logger = logging.getLogger("Recaptcha Controller")

class RecaptchaModel(Schema):
    type = 'object'
    properties = {
        'captchaToken': {
            'type': 'string'
        }
    }

class Recaptcha(Resource):
    PATH = "/recaptcha"

    @swagger.doc({
        'tags': [PERMISSIONS_TAG],
        'description': 'Verify recaptcha',
        'parameters': [
            {
                'name': 'captchaToken',
                'description': 'token generated by the recaptcha for verification',
                'required': True,
                'in': 'body',
                'schema': RecaptchaModel
            }
        ],
        'responses': {
            '200': {
                'description': 'recaptcha verified'
            },
            '400': {
                'description': 'recaptcha verification failure'
            }
        }
    })
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('captchaToken', type=str, required=True)
        args = parser.parse_args()

        isHuman = getCaptchaResults(args['captchaToken'])
        if isHuman:
            return {"message": "recaptcha verified"}, 200
        return {"message": "recaptcha verification failure"}, 400
