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
        parser.add_argument('levelOfStudy', type=str, required=True)
        parser.add_argument('birthday', type=convertDatetimeToString, required=True)
        parser.add_argument('shirtSize', type=str, required=True)
        parser.add_argument('hasAttendedWiCHacks', type=bool, required=True)
        parser.add_argument('hasAttendedHackathons', type=bool, required=True)
        parser.add_argument('university', type=str, required=True)
        parser.add_argument('gender', type=str, required=True)
        parser.add_argument('busRider', type=bool, required=True)
        parser.add_argument('busStop', type=str, required=False)
        parser.add_argument('dietaryRestrictions', type=str, required=False)
        parser.add_argument('specialAccommodations', type=str, required=False)
        parser.add_argument('affirmedAgreements', type=bool, required=True)
        parser.add_argument('isVirtual', type=bool, required=True)
        args = parser.parse_args()

        applicationCreated = createApplication(auth0_id=auth0_id, major=args['major'],
                                               levelOfStudy=args['levelOfStudy'],
                                               birthday=args['birthday'],
                                               shirtSize=args['shirtSize'],
                                               hasAttendedWiCHacks=args['hasAttendedWiCHacks'],
                                               hasAttendedHackathons=args['hasAttendedHackathons'],
                                               university=args['university'],
                                               gender=args['gender'],
                                               busRider=args['busRider'],
                                               busStop=args['busStop'],
                                               dietaryRestrictions=args['dietaryRestrictions'],
                                               specialAccommodations=args['specialAccommodations'],
                                               affirmedAgreements=args['affirmedAgreements'],
                                               isVirtual=args["isVirtual"]
                                               )
        if applicationCreated is None:
            return {"message": "Internal Server Error"}, 500
        elif not applicationCreated:
            # creating application and linking to user failed
            return {"message": "Internal Server Error"}, 500
        return {}, 200
