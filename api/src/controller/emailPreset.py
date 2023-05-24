from flask_restful import Resource
from flask import request
from flask_restful_swagger_2 import swagger

from controller.email import EmailPartialFailureResponseModel
from utils.authentication import authenticate
from data.permissions import canSendEmails
from data.email import sendPresetEmail
from utils.swagger import EMAILS_TAG


class EmailPreset(Resource):
    PATH = '/email/preset/<emailName>'

    @swagger.doc({
        'summary': "send preset email",
        'tags': [EMAILS_TAG],
        'description': "Send a preset email",
        'parameters': [
            {
                'name': 'emailName',
                'description': 'Name of preset email to send. Ex: "ACCEPTED","REJECTED","CONFIRMED"',
                'required': True,
                'in': 'path',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'Emails successfully sent'
            },
            '500': {
                'description': 'DB querying or email sending failure',
                'schema': EmailPartialFailureResponseModel
            }
        }
    })
    def post(self, emailName):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canSendEmails(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        failedEmailList, didSucceed = sendPresetEmail(emailName)
        if didSucceed:
            return {"message": "Email Successfully Sent"}
        else:
            return {"message": "Email Failed", "failedEmailAddresses": failedEmailList}, 500
