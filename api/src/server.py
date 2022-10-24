import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from controller.healthcheck import Healthcheck
from controller.test import Test
from db.migration import migration
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
cors = CORS(app)  # , resources={r"/*": {"origins": "localhost:3000"}}
load_dotenv()

api.add_resource(Healthcheck, '/')
api.add_resource(Test, '/userTest/<id>')

if not (migration.initializeMigrations() and migration.up()):
    logger.error("Migration Failure")
    sys.exit(1)
logger.info("Starting Server")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5002')
