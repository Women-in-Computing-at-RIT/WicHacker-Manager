import logging

from flask_restful import reqparse
from flask import request
from data.users import getUserByUserID, getUserByAuthID
from data.createUser import createUser
from utils.authentication import authenticate
from data.validation import validatePhoneNumberString, validateEmailAddress
from data.permissions import canAccessUserData, canUpdateApplicationStatus
from flask_restful_swagger_2 import swagger, Resource
from utils.swagger import USERS_TAG, UserResponseModel, UserModel

logger = logging.getLogger("User")

def getUserParser() -> reqparse.RequestParser:
    """
    Method to get request parser for requests with a user in the body
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument('firstName', type=str, required=True)
    parser.add_argument('lastName', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('phoneNumber', type=str, required=True, help="format agnostic phone number")
    return parser

class User(Resource):
    PATH = '/user'
    PATH_WITH_ID = '/user/id/<user_id>'

    @swagger.doc({
        'tags': [USERS_TAG],
        'description': "Create a new user",
        'reqparser': {'name': 'ShortenedUserModel', 'parser': getUserParser()},
        'responses': {
            '200': {
                'description': 'User Created Successfully',
                'schema': UserResponseModel
            }
        }
    })
    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        # Parse request body
        args = getUserParser().parse_args()

        # Validate phone number and email
        if not (validatePhoneNumberString(args['phoneNumber']) and validateEmailAddress(args['email'])):
            return {"message": "Phone Number or Email Invalid"}, 400

        userId = createUser(auth0_id, firstName=args['firstName'], lastName=args['lastName'], email=args['email'], phoneNumber=args['phoneNumber'])
        if userId is None:
            return {"message": "Internal Server Error"}, 500
        return {"user_id": userId}, 200

    @swagger.doc({
        'tags': [USERS_TAG],
        'description': 'Get information from user. Defaults to self if user_id not provided',
        'parameters': [
            {
                'name': 'user_id',
                'description': 'Optional WiCHacks User ID',
                'required': False,
                'in': 'path',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'user information',
                'schema': UserModel
            }
        }
    })
    def get(self, user_id=None):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']
        if user_id is None:
            # targeting current user, query based on auth id
            userData = getUserByAuthID(auth0_id)
            if userData is None:
                return {"message": "User not Found"}, 400
            if len(userData.keys()) == 0:
                # User created in Auth0 but not in WiCHacker Manager
                return None, 204
            return userData

        # =========================
        # Permissions Required
        # =========================
        permissions = canAccessUserData(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        # User has permission
        userData = getUserByUserID(user_id)
        if userData is None:
            return {"message": "User Could Not Be Found"}, 400
        return userData
