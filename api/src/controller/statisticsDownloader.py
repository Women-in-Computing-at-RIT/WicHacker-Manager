import logging
import io
import csv

import flask.helpers
from flask_restful import Resource
from flask import request, make_response
from flask_restful_swagger_2 import swagger

from utils.authentication import authenticate
from data.permissions import canViewStatistics
from data.statistics import getHackerStatistics

logger = logging.getLogger("Downloader")


class StatisticsDownloader(Resource):
    PATH = '/downloads/statistics/<stat>'

    @swagger.doc({
        'summary': "get user information",
        'tags': ["Statistics"],
        'description': 'Download csv with specific statistic. Statistics to download include applications, schools, '
                       'shirts, busStops, and isVirtual',
        'parameters': [
            {
                'name': 'stat',
                'description': 'Which statistic to download',
                'required': False,
                'in': 'path',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'user information'
            }
        }
    })
    def get(self, stat):
        """
        Endpoint to download csv with statistic in it. Statistic options include 'applications', 'schools', 'shirts',
        'busStops', and 'isVirtual'
        :param stat:
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

        # get all event statistics
        statistics = getHackerStatistics()
        if statistics is None:
            return {"message": "Internal Server Error"}, 500

        # check that specific statistic for downloading exists
        if statistics.get(stat, default=None) is None:
            return {"message": "Statistic does not exist"}, 400

        # write csv into Response and return
        return StatisticsDownloader.csvDictWriterHelper(statistics[stat])

    @staticmethod
    def csvDictWriterHelper(data: dict) -> flask.helpers.Response:
        """
        Helper function to write an un-nested dictionary of data to a csv file
        :param data:
        :return: flask.helpers.Response object that contains csv file
        """

        outputString = io.StringIO()
        dictWriter = csv.DictWriter(outputString, fieldnames=list(data.keys()))
        dictWriter.writeheader()
        dictWriter.writerow(data)

        response = make_response()
        response.status_code = 200
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.headers["Content-type"] = "text/csv"
        return response
