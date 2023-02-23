import logging

from flask_restful import Resource
from flask import request
from utils.authentication import authenticate
from data.discord import getHackerDataByDiscordId

logger = logging.getLogger("Discord")
class Discord(Resource):
    PATH = '/discord/user/<discord_id>'

    def get(self, discord_id):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Must be logged in"}, 401
        if not authenticationPayload['gty'] == 'client-credentials':
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