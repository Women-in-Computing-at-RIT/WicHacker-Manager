from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUserByUserID, getUserByAuthID
from utils.authErrorHandler import AuthError, handle_auth_error
from utils.authentication import authenticate

class User(Resource):
    PATH = '/user'
    PATH_WITH_ID = '/user/<user_id>'

    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload.sub

        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str, required=True)
        parser.add_argument('lastName', type=str, required=True)
        parser.add_argument('pronouns', type=str, required=True)
        parser.add_argument('isVirtual', type=bool, required=True)
        args = parser.parse_args()

        userId = createUser(auth0_id, firstName=args['firstName'], lastName=args['lastName'],
                                pronouns=args['pronouns'], is_virtual=args['isVirtual'])
        if userId is None:
            return {"message": "Internal Server Error"}, 500
        return {"user_id": userId}, 200



    def get(self, user_id=None):
        if user_id is None:
            # targeting current user, set user_id based on token
            try:
                authenticationPayload = authenticate(request.headers)
            except AuthError as error:
                return handle_auth_error(error)
            if authenticationPayload is None:
                return {"message": "Must be logged in"}, 400
            auth0_id = authenticationPayload.sub
            userData = getUserByAuthID(auth0_id)
            if userData is None:
                return {"message": "User not Found"}, 400
            return userData
        # get info on user with user_id
        userData = getUserByUserID(user_id)
        if userData is None:
            return {"message": "User Data Unable to be Returned"}, 400
        return userData