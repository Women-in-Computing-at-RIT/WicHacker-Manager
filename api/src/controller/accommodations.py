import logging

from flask import request
from flask_restful import Resource

from utils.authentication import authenticate
from data.permissions import canViewStatistics
from data.statistics import getHackerAccommodations
from flask_restful_swagger_3 import swagger

logger = logging.getLogger("Statistics")


class Accommodations(Resource):
    PATH = '/accommodations'

    def get(self):
        """
        Get Hacker Accommodations
        :return:
        """
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canViewStatistics(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        statistics = getHackerAccommodations()
        if statistics is None:
            return {"message": "Internal Server Error"}, 500
        return statistics, 200
