from unittest.mock import patch
import json


from controller.users import Users

# client imported for side effects
from test.testSetupHelper import client


@patch('controller.user.authenticate')
@patch('data.users.exec_get_all')
def test_get_users_successfully(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = [{"user_id": 5, "first_name": "Lenny"}]
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(Users.PATH)

    # Validate
    assert response.status_code == 200
    assert json.loads(response.data)[0]["first_name"] == "Lenny"

@patch('controller.user.authenticate')
@patch('data.users.exec_get_all')
def test_get_users_failed(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = None
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(Users.PATH)

    # Validate
    assert response.status_code == 400