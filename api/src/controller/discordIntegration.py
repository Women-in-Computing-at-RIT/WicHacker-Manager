import logging

import requests
from flask_restful import Resource
from flask import request, redirect
from flask_restful_swagger_2 import swagger

from data.users import getUserByAuthID, getUserIdFromAuthID
from utils.authentication import authenticate
from data.discord import saveDiscordId
from urllib.parse import quote
from hashlib import sha256
from utils.aws import getDiscordClientID, getDiscordClientSecret, getRedirectDomain
from utils.swagger import DISCORD_TAG

logger = logging.getLogger("Discord")


def getRedirectUrl():
    # @TODO find true solution for hotfix
    # return getRedirectDomain() + "/discord/callback"
    return getRedirectDomain()


def getUrlSafeRedirectUrl():
    url = getRedirectUrl()
    return quote(url, safe='')


class DiscordIntegration(Resource):
    PATH = '/discord'

    @swagger.doc({
        'tags': [DISCORD_TAG],
        'description': "Get redirect to discord authorization page",
        'parameters': [
            {
                'name': 'id',
                'description': 'WiCHacks User ID',
                'required': True,
                'in': 'query',
                'type': 'integer'
            }
        ],
        'responses': {
            '302': {
                'description': 'redirecting user'
            }
        }
    })
    def get(self):
        userId = request.args.get('id')
        if userId is None:
            return {}, 400

        state = sha256(str(userId).encode("ASCII")).hexdigest()
        urlEncodedCallback = getUrlSafeRedirectUrl()
        discordAuthorizationURL = f'https://discord.com/oauth2/authorize?response_type=code&client_id={getDiscordClientID()}&scope=identify&state={state}&redirect_uri={urlEncodedCallback}'
        return redirect(discordAuthorizationURL, code=302)

    @swagger.doc({
        'tags': [DISCORD_TAG],
        'description': "callback endpoint from discord integration to connect WiCHacks Hacker with a Discord User",
        'parameters': [
            {
                'name': 'code',
                'description': 'Discord auth code',
                'required': True,
                'in': 'query',
                'type': 'string'
            },
            {
                'name': 'state',
                'description': 'Encoded WiCHacks user id to ensure no attacks on the hacker',
                'required': True,
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'integration successful'
            }
        }
    })
    def post(self):
        """
        2nd part of discord oauth integration to retrieve hacker's discord id
        :return:
        """
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']
        userId = getUserIdFromAuthID(auth0_id)

        # verify user data
        state = request.args.get('state')
        code = request.args.get('code')
        if not state == sha256(str(userId).encode("ASCII")).hexdigest():
            user = getUserByAuthID(auth0_id)
            logger.error("A Hacker is under a CSRF attack. user=%s", user)
            return {}, 400
        if code is None:
            return {}, 400

        # get discord auth token for user
        payload = {
            'client_id': getDiscordClientID(),
            'client_secret': getDiscordClientSecret(),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': getRedirectUrl()
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://discord.com/api/oauth2/token', data=payload, headers=headers)
        discordData = response.json()
        if not response.status_code == 200:
            logger.error("Requesting Token from code Failure: UserId=%s", userId)
            return {}, 500
        hackerAccessToken = discordData['access_token']

        # user hacker discord auth token to retrieve discord id
        headers = {
            'authorization': 'Bearer ' + hackerAccessToken
        }
        identityResponse = requests.get("https://discord.com/api/users/@me", headers=headers)
        if not identityResponse.status_code == 200:
            logger.error("Requesting Identity from Discord Failed: UserId=%s", userId)
            return {}, 500
        userDiscordId = identityResponse.json()['id']

        # save discord id
        saveSuccessful = saveDiscordId(auth0Id=auth0_id, discordId=userDiscordId)
        if saveSuccessful:
            return {"Message": "Discord Integration Success"}
        return {}, 500
