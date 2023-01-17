import logging

from flask_restful import Resource, reqparse
from flask import request
from data.recaptcha import getCaptchaResults

logger = logging.getLogger("Recaptcha Controller")

class Recaptcha(Resource):
    PATH = "/recaptcha"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('captchaToken', type=str, required=True)
        args = parser.parse_args()

        isHuman = getCaptchaResults(args['captchaToken'])
        if isHuman:
            return {"message": "recaptcha verified"}, 200
        return {"message": "recaptcha verification failure"}, 400
