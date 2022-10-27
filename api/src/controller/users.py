from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUser


class Users(Resource):
    def post(self):
        return "Not Implemented Yet", 415

    def get(self):
        return "Not Implemented Yet", 415


