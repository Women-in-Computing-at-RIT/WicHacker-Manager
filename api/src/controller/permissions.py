import http
import logging

from flask_restful import Resource, reqparse
from flask import request
from utils.authentication import authenticate
from data.permissions import checkUserPermissionsByAuth0Id

logger = logging.getLogger("Recaptcha Controller")


class Permissions(Resource):
    PATH = "/permission/<permission>/<accessType>"

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

