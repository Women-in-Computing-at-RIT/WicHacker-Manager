from flask_restful import Resource, reqparse
from flask import request

from data.users import getUserEmailsWithFilter
from utils.authentication import authenticate, getAuthToken
from data.permissions import canSendEmails
from data.email import sendPresetEmail


class EmailPreset(Resource):
    PATH = '/email/preset/<emailName>'

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
