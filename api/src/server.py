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
from controller.recaptcha import Recaptcha
from controller.permissions import Permissions
from controller.statistics import Statistics
from controller.accommodations import Accommodations
from controller.email import Email
from controller.emailPreset import EmailPreset
from controller.confirmation import Confirmation
from db.migration import migration
import logging
from dotenv import load_dotenv
from utils.authErrorHandler import handle_auth_error, AuthError
from utils.genericErrorHandler import handle_error
from utils.aws import initializeAWSClients
from db.db_utils import initializeDBSecrets
from utils.authentication import initializeAuthentication

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
api.add_resource(Recaptcha, Recaptcha.PATH)
api.add_resource(Permissions, Permissions.PATH)
api.add_resource(Statistics, Statistics.PATH)
api.add_resource(Accommodations, Accommodations.PATH)
api.add_resource(Email, Email.PATH)
api.add_resource(EmailPreset, EmailPreset.PATH)
api.add_resource(Confirmation, Confirmation.PATH)

if not initializeAWSClients():
    logger.error("AWS Client Initialization Failure")
    sys.exit(1)
if not initializeDBSecrets():
    logger.error("Initializing DB Secrets Failure")
    sys.exit(1)
if not migration.initializeMigrations():
    logger.error("Initialize Migration Failure")
    sys.exit(1)
if not migration.up():
    logger.error("Migration Failure")
    sys.exit(1)
if not initializeAuthentication():
    logger.error("Authentication Initialization Failure")
    sys.exit(1)
logger.info("Starting Server")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
