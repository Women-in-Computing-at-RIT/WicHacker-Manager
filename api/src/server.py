import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from controller.healthcheck import Healthcheck
from controller.test import Test
from controller.user import User
from controller.users import Users
from db.migration import migration
import logging
from dotenv import load_dotenv
from utils.authErrorHandler import handle_auth_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = Flask(__name__)
app.register_error_handler(401, handle_auth_error)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
cors = CORS(app)  # , resources={r"/*": {"origins": "localhost:3000"}}
load_dotenv()

api.add_resource(Healthcheck, Healthcheck.PATH)
api.add_resource(Test, Test.PATH)
api.add_resource(User, User.PATH, endpoint="user")
api.add_resource(User, User.PATH_WITH_ID, endpoint="user_with_id")
api.add_resource(Users, Users.PATH)

if not (migration.initializeMigrations() and migration.up()):
    logger.error("Migration Failure")
    sys.exit(1)
logger.info("Starting Server")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
