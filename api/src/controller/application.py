import logging

from flask_restful import Resource, reqparse
from flask import request
from data.application import createApplication, updateApplication
from data.users import getUserByUserID
from utils.authentication import authenticate
from data.permissions import canUpdateApplicationStatus

logger = logging.getLogger("Application")


class Application(Resource):
    PATH = '/user/application'

    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        parser = reqparse.RequestParser()
        parser.add_argument('major', type=str, required=True)
        parser.add_argument('levelOfStudy', type=str, required=True)
        parser.add_argument('age', type=int, required=True)
        parser.add_argument('shirtSize', type=str, required=True)
        parser.add_argument('hasAttendedWiCHacks', type=bool, required=True)
        parser.add_argument('hasAttendedHackathons', type=bool, required=True)
        parser.add_argument('university', type=str, required=True)
        parser.add_argument('gender', type=str, required=True)
        parser.add_argument('busRider', type=bool, required=True)
        parser.add_argument('busStop', type=str, required=False, default=False)
        parser.add_argument('dietaryRestrictions', type=str, required=False, default=None)
        parser.add_argument('specialAccommodations', type=str, required=False, default=None)
        parser.add_argument('affirmedAgreements', type=bool, required=True)
        parser.add_argument('isVirtual', type=bool, required=True)
        parser.add_argument('mlhEmailsAllowed', type=bool, required=False)
        args = parser.parse_args()

        applicationCreated = createApplication(auth0_id=auth0_id, major=args['major'],
                                               levelOfStudy=args['levelOfStudy'],
                                               age=args['age'],
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
                                               isVirtual=args["isVirtual"],
                                               mlhEmailsAllowed=args.get("mlhEmailsAllowed", False)
                                               )
        if applicationCreated is None:
            return {"message": "Experienced Internal Server Error"}, 500
        elif not applicationCreated:
            # creating application and linking to user failed
            return {"message": "Internal Server Error"}, 500
        return {}, 200

    def put(self):
        """
        UserID in body is the user id of the user that will be updated
        Update performed by getting user data, updating if that data is in the body, and then save the user data back to database
        :return:
        """
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canUpdateApplicationStatus(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=int, required=True)
        parser.add_argument('major', type=str, required=False)
        parser.add_argument('levelOfStudy', type=str, required=False)
        parser.add_argument('age', type=int, required=False)
        parser.add_argument('shirtSize', type=str, required=False)
        parser.add_argument('hasAttendedWiCHacks', type=bool, required=False)
        parser.add_argument('hasAttendedHackathons', type=bool, required=False)
        parser.add_argument('university', type=str, required=False)
        parser.add_argument('gender', type=str, required=False)
        parser.add_argument('busRider', type=bool, required=False)
        parser.add_argument('busStop', type=str, required=False, default=None)
        parser.add_argument('dietaryRestrictions', type=str, required=False, default=None)
        parser.add_argument('specialAccommodations', type=str, required=False, default=None)
        parser.add_argument('affirmedAgreements', type=bool, required=False)
        parser.add_argument('isVirtual', type=bool, required=False)
        parser.add_argument('mlhEmailsAllowed', type=bool, required=False)
        args = parser.parse_args()

        userId = args['user_id']
        userData = getUserByUserID(userId)
        # update application by supplementing passed in data to update with current user data and saving everything
        applicationUpdated = updateApplication(applicationId=userData['application_id'],
                                               major=args.get('major', userData['major']),
                                               levelOfStudy=args.get('levelOfStudy', userData['level_of_study']),
                                               age=args.get('age', userData['age']),
                                               shirtSize=args.get('shirtSize', userData['shirt_size']),
                                               hasAttendedWiCHacks=args.get('hasAttendedWiCHacks', userData['has_attended_wichacks']),
                                               hasAttendedHackathons=args.get('hasAttendedHackathons', userData['has_attended_hackathons']),
                                               university=args.get('university', userData['university']),
                                               gender=args.get('gender', userData['gender']),
                                               busRider=args.get('busRider', userData['bus_rider']),
                                               busStop=args.get('busStop', userData['bus_stop']),
                                               dietaryRestrictions=args.get('dietaryRestrictions', userData['dietary_restrictions']),
                                               specialAccommodations=args.get('specialAccommodations', userData['special_accommodations']),
                                               affirmedAgreements=args.get('affirmedAgreements', userData['affirmed_agreements']),
                                               isVirtual=args.get("isVirtual", userData['is_virtual']),
                                               mlhEmailsAllowed=args.get("mlhEmailsAllowed", userData['allowMlhEmails'])
                                               )
        if applicationUpdated is None:
            return {"message": "Internal Server Error"}, 500
        elif not applicationUpdated:
            # creating application and linking to user failed
            return {"message": "Application Update Failure"}, 400
        return {"message": "Application Updated"}, 200
