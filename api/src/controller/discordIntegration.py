import logging

import requests
from flask_restful import Resource
from flask import request, redirect
from data.users import getUserByAuthID, getUserIdFromAuthID
from utils.authentication import authenticate
from data.discord import saveDiscordId
from urllib.parse import quote
from hashlib import sha256
from utils.aws import getDiscordClientID, getDiscordClientSecret, getRedirectDomain

logger = logging.getLogger("Discord")


def getRedirectUrl():
    return getRedirectDomain() + "/discord/callback"


def getUrlSafeRedirectUrl():
    url = getRedirectUrl()
    return quote(url, safe='')


class DiscordIntegration(Resource):
    PATH = '/discord'

    def get(self):
        userId = request.args.get('id')
        if userId is None:
            return {}, 400

        state = sha256(str(userId).encode("ASCII")).hexdigest()
        urlEncodedCallback = getUrlSafeRedirectUrl()
        discordAuthorizationURL = f'https://discord.com/oauth2/authorize?response_type=code&client_id={getDiscordClientID()}&scope=identify&state={state}&redirect_uri={urlEncodedCallback}'
        return redirect(discordAuthorizationURL, code=302)

    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']
        userId = getUserIdFromAuthID(auth0_id)

        state = request.args.get('state')
        code = request.args.get('code')
        if not state == sha256(str(userId).encode("ASCII")).hexdigest():
            user = getUserByAuthID(auth0_id)
            logger.error("A Hacker is under a CSRF attack. user=%s", user)
            return {}, 400
        if code is None:
            return {}, 400

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
        headers = {
            'authorization': 'Bearer ' + hackerAccessToken
        }
        identityResponse = requests.get("https://discord.com/api/users/@me", headers=headers)
        if not identityResponse.status_code == 200:
            logger.error("Requesting Identity from Discord Failed: UserId=%s", userId)
            return {}, 500
        userDiscordId = identityResponse.json()['id']
        saveSuccessful = saveDiscordId(auth0Id=auth0_id, discordId=userDiscordId)
        if saveSuccessful:
            return {"Message": "Discord Integration Success"}
        return {}, 500
