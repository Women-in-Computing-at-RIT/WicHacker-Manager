from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUser
from utils.authentication import authenticate_user, getAuthToken

class Test(Resource):
    def get(self, id):
        print("user_id: " + id)

        auth_token = getAuthToken(request.headers)
        if auth_token is None:
            return "Authorization Header Failure", 200
        isAuthenticated = authenticate_user(auth_token)
        if not isAuthenticated:
            return "Authentication Failure", 200

        return "Successfully authenticated", 200


