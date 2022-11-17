import pytest
from flask import Flask
from flask_restful import Api

from controller.healthcheck import Healthcheck
from controller.test import Test
from controller.user import User
from controller.users import Users
from utils.authErrorHandler import AuthError, handle_auth_error
from utils.genericErrorHandler import handle_error


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_error_handler(AuthError, handle_auth_error)
    app.register_error_handler(Exception, handle_error)
    api = Api(app)

    api.add_resource(Healthcheck, Healthcheck.PATH)
    api.add_resource(Test, Test.PATH)
    api.add_resource(User, User.PATH, endpoint="user")
    api.add_resource(User, User.PATH_WITH_ID, endpoint="user_with_id")
    api.add_resource(Users, Users.PATH)
    return app.test_client()