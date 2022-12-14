import logging
from flask import make_response

from utils.authErrorHandler import AuthError, handle_auth_error

logger = logging.getLogger("error_handler")


def handle_error(ex):
    logger.error(ex)
    response = make_response({"message": "whoops...something went wrong"}, 500)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    return response
