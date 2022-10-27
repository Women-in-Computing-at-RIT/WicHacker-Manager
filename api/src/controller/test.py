from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUser
from utils.authentication import authenticate, getAuthToken

class Test(Resource):
    def get(self, id):
        print("user_id: " + id)

        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return "Authorization Header Failure", 401
        return "Successfully authenticated", 200


