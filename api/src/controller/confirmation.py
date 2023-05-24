import logging

from flask_restful import Resource
from flask import request
from flask_restful_swagger_2 import swagger

from data.application import updateApplication
from data.users import getUserByAuthID, getUserIdFromAuthID
from utils.authentication import authenticate
from data.email import sendConfirmedEmail, CONFIRMED, ACCEPTED
from utils.swagger import APPLICATIONS_TAG

logger = logging.getLogger("Confirmation")


class Confirmation(Resource):
    PATH = '/user/application/confirm'

    @swagger.doc({
        'summary': "confirm attendance for hacker",
        'tags': [APPLICATIONS_TAG],
        'description': "Update application status to confirmed if able",
        'responses': {
            '200': {
                'description': 'Application Status Updated Successfully'
            }
        }
    })
    def post(self):
        """
        Update user application status to CONFIRMED
        :return:
        """
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        userData = getUserByAuthID(auth0_id)
        if userData is None:
            return {"message": "Internal Server Error"}, 500
        if len(userData.keys()) == 0:
            return {"message": "Could Not Find User"}, 400
        if not userData['status'] == ACCEPTED:
            if userData['status'] == CONFIRMED:
                return {"message": "User Already Confirmed"}
            return {"message": "User Status Failed"}, 400

        # update status by retrieving and re-saving application
        applicationUpdated = updateApplication(applicationId=userData['application_id'],
                                               status=CONFIRMED,
                                               major=userData['major'],
                                               levelOfStudy=userData['level_of_study'],
                                               age=userData['age'],
                                               shirtSize=userData['shirt_size'],
                                               hasAttendedWiCHacks=userData['has_attended_wichacks'],
                                               hasAttendedHackathons=userData['has_attended_hackathons'],
                                               university=userData['university'],
                                               gender=userData['gender'],
                                               busRider=userData['bus_rider'],
                                               busStop=userData['bus_stop'],
                                               dietaryRestrictions=userData['dietary_restrictions'],
                                               specialAccommodations=userData['special_accommodations'],
                                               affirmedAgreements=userData['affirmed_agreements'],
                                               isVirtual=userData['is_virtual'],
                                               mlhEmailsAllowed=userData['allowMlhEmails']
                                               )
        if applicationUpdated is None:
            return {"message": "Internal Server Error"}, 500
        elif not applicationUpdated:
            return {"message": "Application Update Failure"}, 400

        sendConfirmedEmail(getUserIdFromAuthID(auth_id=auth0_id))
        return {"message": "Application Updated"}, 200
