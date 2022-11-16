from flask_restful import Resource, reqparse
from flask import request
from utils.authentication import authenticate, getAuthToken

class Test(Resource):

    PATH = '/userTest/<id>'
    def get(self, id):
        print("user_id: " + id)

        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        return {"message": "Successfully authenticated"}, 200


