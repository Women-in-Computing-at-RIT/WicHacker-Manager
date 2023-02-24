from flask_restful import Resource, reqparse
from flask import request
from data.users import getUsers
from utils.authentication import authenticate
from data.permissions import canAccessUserData


class UserSearch(Resource):
    PATH = '/user/search'

    def get(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canAccessUserData(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not (permissions or authenticationPayload['gty'] == 'client-credentials'):
            # check that the grant type is client-credentials which will exist only for the machine to machine
            # auth0 connections using client id and secret, aka: discord bots and s3 resume downloader
            return {"message": "Permission Denied"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str, required=False)
        parser.add_argument('lastName', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('applicationId', type=str, required=False)
        parser.add_argument('userId', type=str, required=False)
        parser.add_argument('recipientStatusFilter', type=str, required=False, action="append")
        args = parser.parse_args()

        matchingUsers = getUsers(applicationStatusFilterList=args['recipientStatusFilter'],
                                 firstName=args['firstName'],
                                 lastName=args['lastName'],
                                 email=args['email'],
                                 applicationId=args['applicationId'],
                                 userId=args['userId'])

        if matchingUsers is None:
            return {"Message": "Internal Server Error"}, 500
        return matchingUsers