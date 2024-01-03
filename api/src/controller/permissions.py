import http
import logging

from flask_restful import Resource, reqparse
from flask import request
from flask_restful_swagger_2 import swagger

from utils.authentication import authenticate
from data.permissions import checkUserPermissionsByAuth0Id
from utils.swagger import PERMISSIONS_TAG

logger = logging.getLogger("Permissions Controller")


class Permissions(Resource):
    PATH = "/permission/<permission>/<accessType>"

    @swagger.doc({
        'summary': "check user permissions",
        'tags': [PERMISSIONS_TAG],
        'description': 'check if user has access',
        'parameters': [
            {
                'name': 'permission',
                'description': 'What the user is attempting to access',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'accessType',
                'description': 'Type of access the user wants. Ex: READ or WRITE',
                'required': True,
                'in': 'path',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'User has access to the requested item'
            },
            '403': {
                'description': "User does not have access to the requested item"
            }
        }
    })
    def get(self, permission, accessType):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']

        if permission is None or accessType is None:
            return {"message": "Data Format Error"}, 400

        hasPermission = checkUserPermissionsByAuth0Id(auth0Id=auth0_id, permission=permission, accessType=accessType)
        if hasPermission is None:
            return {"message": "Internal Server Error"}, 500
        if hasPermission:
            return {"message": "User has Permissions"}, 200
        return {"message", "Permission Denied"}, 403

