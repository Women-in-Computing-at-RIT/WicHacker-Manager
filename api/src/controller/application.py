import logging

from flask_restful import Resource, reqparse
from flask import request
from data.application import createApplication
from utils.authentication import authenticate
from utils.convertDatetime import convertDatetimeToString
from datetime import datetime

logger = logging.getLogger("Application")


class Application(Resource):
    PATH = '/user/apply'

    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        parser = reqparse.RequestParser()
        parser.add_argument('major', type=str, required=True)
        parser.add_argument('year', type=str, required=True)
        parser.add_argument('birthday', type=convertDatetimeToString, required=True)
        parser.add_argument('resume', type=str, required=True)
        parser.add_argument('shirtSize', type=str, required=True)
        parser.add_argument('hasAttendedWiCHacks', type=bool, required=True)
        parser.add_argument('university', type=str, required=True)
        args = parser.parse_args()

        applicationCreated = createApplication(auth0_id=auth0_id, major=args['major'], year=args['year'],
                                               birthday=args['birthday'], resumeLink=args['resume'],
                                               shirtSize=args['shirtSize'],
                                               hasPreviouslyAttended=args['hasAttendedWiCHacks'],
                                               university=args['university'])
        if applicationCreated is None:
            return {"message": "Internal Server Error"}, 500
        elif not applicationCreated:
            # creating application and linking to user failed
            return {"message": "Internal Server Error"}, 500
        return {}, 200
