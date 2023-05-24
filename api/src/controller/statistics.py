import logging

from flask_restful import Resource
from flask import request
from flask_restful_swagger_2 import swagger

from utils.authentication import authenticate
from data.permissions import canViewStatistics
from data.statistics import getHackerStatistics
from utils.swagger import STATISTICS_TAG

logger = logging.getLogger("Statistics")


class Statistics(Resource):
    PATH = '/statistics'

    @swagger.doc({
        'summary': "get event statistics",
        'tags': [STATISTICS_TAG],
        'description': "Get statistics for the event",
        'responses': {
            '200': {
                'description': "event statistics",
                'examples': {
                    "application/json": {
                        "applications": {
                            "APPLIED": 13,
                            "ACCEPTED": 5,
                            "CONFIRMED": 2,
                            "REJECTED": 1
                        },
                        "schools": {
                            "School1": 3,
                            "School2": 1,
                            "School3": 1,
                            "School4": 1,
                            "School5": 1
                        },
                        "schoolCount": 5,
                        "shirts": {},
                        "busStops": {
                            "School 1": 1,
                            "School 2": 1,
                            "School 3": 1
                        },
                        "isVirtual": {
                            "null": 1,
                            "1": 6
                        }
                    }
                }
            }
        }
    })
    def get(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        auth0_id = authenticationPayload['sub']

        permissions = canViewStatistics(auth0_id)
        if permissions is None:
            return {"message": "Internal Server Error"}, 500
        if not permissions:
            return {"message": "Permission Denied"}, 403

        statistics = getHackerStatistics()
        if statistics is None:
            return {"message": "Internal Server Error"}, 500
        return statistics, 200
