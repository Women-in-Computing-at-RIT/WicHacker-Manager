import json
import sys

from flask import Flask, render_template
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from controller.application import Application
from controller.healthcheck import Healthcheck
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
from controller.userSearch import UserSearch
from controller.discordIntegration import DiscordIntegration
from controller.discord import Discord
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

app = Flask(__name__,
            static_url_path='',
            static_folder='swagger/static',
            template_folder='swagger/templates')
app.register_error_handler(AuthError, handle_auth_error)
app.register_error_handler(Exception, handle_error)
app.config['BUNDLE_ERRORS'] = True
api = Api(app,
          title="WiCHacker Manager API",
          api_spec_url="/docs/api/swagger",
          )
cors = CORS(app)  # , resources={r"/*": {"origins": "localhost:3000"}}
load_dotenv()

api.add_resource(Healthcheck, Healthcheck.PATH)
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
api.add_resource(UserSearch, UserSearch.PATH)
api.add_resource(DiscordIntegration, DiscordIntegration.PATH)
api.add_resource(Discord, Discord.PATH)


@app.route("/docs/swagger")
def testSwagger():
    """
    Serves up swagger page
    :return:
    """
    return render_template("swaggerui.html")


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


def writeSwaggerDoc():
    """
    Generates swagger docs from annotations
    :return:
    """
    logger.info("Writing Swagger Docs")
    with open("src/swagger/static/swagger.json", "w") as file:
        swaggerDict = api.get_swagger_doc()

        # Exception for getting users because of how I implemented the overloading of the get method
        swaggerDict["paths"]["/user/id/{user_id}"].pop('post', None)

        file.write(json.dumps(swaggerDict))


if __name__ == '__main__':
    writeSwaggerDoc()
    logger.info("Starting Server")
    app.run(debug=True, host='0.0.0.0')
