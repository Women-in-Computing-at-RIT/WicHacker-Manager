from flask_restful import Resource, reqparse
from flask import request
from flask_restful_swagger_2 import swagger, Schema

from data.users import getUserEmailsWithFilter
from utils.authentication import authenticate
from data.permissions import canSendEmails
from data.email import sendGroupEmail
from utils.swagger import EMAILS_TAG


class EmailPartialFailureResponseModel(Schema):
    type = "object"
    properties = {
        "failedEmailAddresses": {
            'type': 'array',
            'items': {
                "type": "string"
            },
            'description': "list of email addresses that failed to send or None if failure occurred before emails "
                           "were sent"
        },
        "message": {
            "type": "string",
            "description": "what happened"
        }
    }


def getEmailParser() -> reqparse.RequestParser:
    """
    Method to get parser for email data
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument('body', type=str, required=True, help="in-line styled HTML body of email to be sent")
    parser.add_argument('subjectLine', type=str, required=True)
    parser.add_argument('recipientStatusFilter', type=str, required=True, action="append",
                        help="csv list of statuses of hackers that will get the email")
    return parser


class Email(Resource):
    PATH = '/email'

    @swagger.doc({
        'tags': [EMAILS_TAG],
        'description': "Send email to hackers based on application status",
        'reqparser': {'name': 'EmailModel', 'parser': getEmailParser()},
        'responses': {
            '200': {
                'description': 'All emails sent successfully'
            },
            '500': {
                'description': 'DB querying or email sending failure',
                'schema': EmailPartialFailureResponseModel
            }
        }
    })
    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canSendEmails(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        # parse request body for email data
        args = getEmailParser().parse_args()
        userEmails = getUserEmailsWithFilter(args['recipientStatusFilter'])

        if len(userEmails) == 0:
            # no recipients
            return {"message": "No Recipients"}, 400

        failedEmailList, didSucceed = sendGroupEmail(emailAddresses=userEmails, subject=args['subjectLine'],
                                                     content=args['body'])
        if didSucceed:
            return {"message": "Email Successfully Sent"}
        else:
            return {"message": "Email Failed", "failedEmailAddresses": failedEmailList}, 500
