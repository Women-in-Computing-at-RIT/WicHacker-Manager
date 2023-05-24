import logging

from flask_restful import Resource
from flask import request
from flask_restful_swagger_2 import swagger

from utils.authentication import authenticate
from data.discord import getHackerDataByDiscordId

from utils.swagger import DISCORD_TAG

logger = logging.getLogger("Discord")


class Discord(Resource):
    PATH = '/discord/user/<discord_id>'

    @swagger.doc({
        'tags': [DISCORD_TAG],
        'description': "Get statistics for the event",
        'responses': {
            '200': {
                'description': "event statistics",
                'examples': {
                    "application/json": {
                        "first_name": "alexander",
                        "last_name": "levie",
                        "status": "CONFIRMED"
                    }
                }
            }
        }
    })
    def get(self, discord_id):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        if not authenticationPayload['gty'] == 'client-credentials':
            # check that the grant type is client-credentials which will exist only for the machine to machine
            # auth0 connections using client id and secret, aka: discord bots
            logger.error("Non-Bot/Non-Client Request to get discord information")
            return {"message": "You shall not pass"}, 403

        if discord_id is None:
            return {"Message": "Must include discord id"}, 400
        # ==========
        # Authentication with Bots via API Keys, auth0 ID doesn't mean anything here
        # ==========

        hackerData = getHackerDataByDiscordId(discord_id)
        if hackerData is None:
            return {}, 500
        return hackerData
