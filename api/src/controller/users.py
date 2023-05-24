from flask_restful import Resource, reqparse
from flask import request
from flask_restful_swagger_2 import swagger

from data.users import getUsers
from utils.authentication import authenticate
from data.permissions import canAccessUserData
from utils.swagger import USERS_TAG, UserModel


class Users(Resource):
    PATH = '/users'

    @swagger.doc({
        'summary': "get all users",
        'tags': [USERS_TAG],
        'description': "Get all users",
        'responses': {
            '200': {
                'description': 'users',
                'schema': UserModel.array()
            }
        }
    })
    def get(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canAccessUserData(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        userData = getUsers()
        if userData is None:
            return {"message": "User Data Unable to be Returned"}, 400
        return userData
