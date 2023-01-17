import json
from six.moves.urllib.request import urlopen
from .authErrorHandler import AuthError

from flask import _request_ctx_stack
from jose import jwt, JWTError
from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier, TokenValidationError
import os
from utils.aws import getAuth0ClientID

domain = None
client_id = None
audience = None

jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
issuer = 'https://{}/'.format(domain)
sv = AsymmetricSignatureVerifier(jwks_url)  # Reusable instance

ALGORITHMS = ["RS256"]

def initializeAuthentication() -> bool:
    global domain, client_id, audience
    domain = os.environ.get("AUTH0_DOMAIN", None)
    client_id = getAuth0ClientID()
    audience = os.environ.get("AUTH0_AUDIENCE", None)
    if domain is None or client_id is None or audience is None:
        return False
    return True


def getAuthToken(headers):
    auth_header = headers.get("Authorization", None)
    if not auth_header:
        return None
    auth_header_components = auth_header.split()

    if auth_header_components[0].lower() != "bearer":
        return None
    elif len(auth_header_components) <= 1 or len(auth_header_components) > 2:
        return None

    token = auth_header_components[1]
    return token


def authenticate(headers):
    token = getAuthToken(headers)
    if token is None:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authentication Token Format Incorrect"}, 401)
    jsonurl = urlopen("https://" + domain + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = None
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Unable to decode authentication"
                             " token."}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=audience,
                issuer="https://" + domain + "/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)

        _request_ctx_stack.top.current_user = payload
        return payload
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 401)
