from flask_restful import Resource, reqparse
from flask import request

from data.users import getUserEmailsWithFilter
from utils.authentication import authenticate, getAuthToken
from data.permissions import canSendEmails
from data.email import sendGroupEmail


class Email(Resource):
    PATH = '/email'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('body', type=str, required=True)
        parser.add_argument('subjectLine', type=str, required=True)
        parser.add_argument('recipientStatusFilter', type=str, required=True, action="append")
        args = parser.parse_args()

        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canSendEmails(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        userEmails = getUserEmailsWithFilter(args['recipientStatusFilter'])

        if len(userEmails) == 0:
            # no recipients
            return {"message": "No Recipients"}, 400

        failedEmailList, didSucceed = sendGroupEmail(emailAddresses=userEmails, subject=args['subjectLine'], content=args['body'])
        if didSucceed:
            return {"message": "Email Successfully Sent"}
        else:
            return {"message": "Email Failed", "failedEmailAddresses": failedEmailList}, 500
