from flask import jsonify, make_response
import logging

logger = logging.getLogger("AuthError")


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def handle_auth_error(ex):
    logger.error(ex.error)
    response = make_response(jsonify(ex.error), 500)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "application/json"
    return response
