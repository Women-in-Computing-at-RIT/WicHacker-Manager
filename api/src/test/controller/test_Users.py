from unittest.mock import Mock, patch

import pytest
from flask import Flask
from flask_restful import Api
import json

from controller.users import User


@pytest.fixture
def client():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(User, User.PATH, endpoint="user")
    api.add_resource(User, User.PATH_WITH_ID, endpoint="user_with_id")
    return app.test_client()


@patch('data.users.exec_get_one')
def test_get_user(mock_db_exec, client):
    # mock object responses
    mock_db_exec.return_value = {"user_id": 5, "first_name": "Lenny"}

    # call endpoint
    print(User.PATH_WITH_ID.replace("<user_id>", "1"))
    response = client.get(User.PATH_WITH_ID.replace("<id>", "1"))

    # Validate
    assert response.status_code == 200
    assert json.loads(response.data)["first_name"] == "Lenny"
