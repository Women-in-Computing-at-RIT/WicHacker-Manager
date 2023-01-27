import logging

from flask_restful import Resource, reqparse
from flask import request
from data.application import createApplication, updateApplication
from data.users import getUserByUserID
from utils.authentication import authenticate
from data.permissions import canUpdateApplicationStatus

logger = logging.getLogger("Application")


def valueOrDefaultIfNone(value, default):
    if value is None:
        return default
    return value


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
        parser.add_argument('status', type=str, required=False)
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

        userId = args['userId']
        userData = getUserByUserID(userId)
        if userData is None:
            return {"message": "Internal Server Error"}, 500
        if len(userData.keys()) == 0:
            return {"message": "Could Not Find User"}, 400
        # update application by supplementing passed in data to update with current user data and saving everything
        applicationUpdated = updateApplication(applicationId=userData['application_id'],
                                               status=valueOrDefaultIfNone(args['status'], userData['status']),
                                               major=valueOrDefaultIfNone(args['major'], userData['major']),
                                               levelOfStudy=valueOrDefaultIfNone(args['levelOfStudy'], userData['level_of_study']),
                                               age=valueOrDefaultIfNone(args['age'], userData['age']),
                                               shirtSize=valueOrDefaultIfNone(args['shirtSize'], userData['shirt_size']),
                                               hasAttendedWiCHacks=valueOrDefaultIfNone(args['hasAttendedWiCHacks'], userData['has_attended_wichacks']),
                                               hasAttendedHackathons=valueOrDefaultIfNone(args['hasAttendedHackathons'], userData['has_attended_hackathons']),
                                               university=valueOrDefaultIfNone(args['university'], userData['university']),
                                               gender=valueOrDefaultIfNone(args['gender'], userData['gender']),
                                               busRider=valueOrDefaultIfNone(args['busRider'], userData['bus_rider']),
                                               busStop=valueOrDefaultIfNone(args['busStop'], userData['bus_stop']),
                                               dietaryRestrictions=valueOrDefaultIfNone(args['dietaryRestrictions'], userData['dietary_restrictions']),
                                               specialAccommodations=valueOrDefaultIfNone(args['specialAccommodations'], userData['special_accommodations']),
                                               affirmedAgreements=valueOrDefaultIfNone(args['affirmedAgreements'], userData['affirmed_agreements']),
                                               isVirtual=valueOrDefaultIfNone(args['isVirtual'], userData['is_virtual']),
                                               mlhEmailsAllowed=valueOrDefaultIfNone(args['mlhEmailsAllowed'], userData['allowMlhEmails'])
                                               )
        if applicationUpdated is None:
            return {"message": "Internal Server Error"}, 500
        elif not applicationUpdated:
            # creating application and linking to user failed
            return {"message": "Application Update Failure"}, 400
        return {"message": "Application Updated"}, 200
