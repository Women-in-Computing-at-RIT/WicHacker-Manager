"""import pytest
from flask import Flask
from flask_restful import Api
import json

from controller.healthcheck import Healthcheck


@pytest.fixture
def client():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Healthcheck, Healthcheck.PATH)
    return app.test_client()


def test_get_healthcheck(client):
    response = client.get(Healthcheck.PATH)

    assert response.status_code == 200
    assert json.loads(response.data)["ping"] == "pong"
"""
