from flask_restful import Resource, reqparse
from flask import request
from data.users import createUser, getUser


class Users(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("firstName", type=str)
        parser.add_argument("lastName", type=str)
        parser.add_argument("pronouns", type=str)

        args = parser.parse_args()
        firstName = args["firstName"]
        lastName = args["lastName"]
        pronouns = args["pronouns"]

        is_created = createUser(firstName, lastName, pronouns)

        if is_created is False:
            return "User Not Created", 400
        return "User Successfully Created", 200

    def get(self):
        auth_id = request.args.get('id')

        userInfo = getUser(auth_id)

        if userInfo is None:
            return "User Not Found", 400

        return {"user": userInfo}, 200


