import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

from controller.application import Application
from controller.healthcheck import Healthcheck
from controller.test import Test
from controller.user import User
from controller.users import Users
from controller.resume import Resume
from db.migration import migration
import logging
from dotenv import load_dotenv
from utils.authErrorHandler import handle_auth_error, AuthError
from utils.genericErrorHandler import handle_error
from utils.aws import initializeAWSClients

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = Flask(__name__)
app.register_error_handler(AuthError, handle_auth_error)
app.register_error_handler(Exception, handle_error)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
cors = CORS(app)  # , resources={r"/*": {"origins": "localhost:3000"}}
load_dotenv()

api.add_resource(Healthcheck, Healthcheck.PATH)
api.add_resource(Test, Test.PATH)
api.add_resource(User, User.PATH, endpoint="user")
api.add_resource(User, User.PATH_WITH_ID, endpoint="user_with_id")
api.add_resource(Users, Users.PATH)
api.add_resource(Application, Application.PATH)
api.add_resource(Resume, Resume.PATH)

if not migration.initializeMigrations():
    logger.error("Initialize Migration Failure")
    sys.exit(1)
if not migration.up():
    logger.error("Migration Failure")
    sys.exit(1)
if not initializeAWSClients():
    logger.error("AWS Client Initialization Failure")
    sys.exit(1)
logger.info("Starting Server")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
