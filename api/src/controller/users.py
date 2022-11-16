from flask_restful import Resource, reqparse
from flask import request
from data.users import getUsers


class Users(Resource):
    PATH = '/users'

    def get(self):
        userData = getUsers()
        if userData is None:
            return {"message": "User Data Unable to be Returned"}, 400
        return userData
