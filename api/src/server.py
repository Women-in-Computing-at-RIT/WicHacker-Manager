import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from api.healthcheck import Healthcheck
from api.users import Users
from api.communities import Communities
from api.channels import Channels
from api.dms import Dms
from api.login import Login
from db.migration import migration
import logging

logger = logging.getLogger("server")

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
cors = CORS(app)  # , resources={r"/*": {"origins": "localhost:3000"}}

api.add_resource(Healthcheck, '/')

if __name__ == '__main__':
    if not migration.initializeMigrations() and migration.up():
        logger.error("Migration Failure")
        sys.exit(1)
    app.run(debug=True)