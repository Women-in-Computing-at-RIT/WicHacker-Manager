from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUserByUserID, getUserByAuthID


class User(Resource):
    PATH = '/user'
    PATH_WITH_ID = '/user/<user_id>'

    def post(self):
        return "Not Implemented Yet", 415

    def get(self, user_id=None):
        if user_id is None:
            # targeting current user, set user_id based on token
            return "Not Implemented Yet", 415
        # get info on user with user_id
        userData = getUserByUserID(user_id)
        if userData is None:
            return "User Data Unable to be Returned", 400
        return userData
