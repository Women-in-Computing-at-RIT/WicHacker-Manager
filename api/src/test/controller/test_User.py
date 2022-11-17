from unittest.mock import patch
import json

from controller.user import User

# client imported for side effects
from test.testSetupHelper import client


@patch('controller.user.authenticate')
@patch('data.users.exec_get_one')
def test_get_user_by_id_successfully(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = ({"user_id": 5, "first_name": "Lenny"}, False)
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(User.PATH_WITH_ID.replace("<id>", "1"))

    # Validate
    assert response.status_code == 200
    assert json.loads(response.data)["first_name"] == "Lenny"


@patch('controller.user.authenticate')
@patch('data.users.exec_get_one')
def test_get_user_successfully(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = ({"user_id": 5, "first_name": "Lenny"}, False)
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(User.PATH)

    # Validate
    assert response.status_code == 200
    assert json.loads(response.data)["first_name"] == "Lenny"


@patch('controller.user.authenticate')
@patch('data.users.exec_get_one')
def test_get_user_successfully(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = (None, True)
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(User.PATH)

    # Validate
    assert response.status_code == 400


@patch('controller.user.authenticate')
@patch('data.users.exec_get_one')
def test_get_user_success_no_content(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = (None, False)
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(User.PATH)

    # Validate
    assert response.status_code == 204


@patch('controller.user.authenticate')
def test_get_user_authentication_error(mock_authenticate, client):
    # mock object responses
    mock_authenticate.return_value = None

    # call endpoint)
    response = client.get(User.PATH)

    # Validate
    assert response.status_code == 401


@patch('controller.user.authenticate')
@patch('data.users.exec_get_one', side_effect=Exception('test exception'))
def test_get_user_with_exception(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.get(User.PATH_WITH_ID.replace("<id>", "1"))

    # Validate
    assert response.status_code == 500


@patch('controller.user.authenticate')
@patch('data.users.exec_commit_return_autoincremented_id')
def test_post_user_successfully(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = 1
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.post(User.PATH, json={'firstName': 'testFirstName',
                                                'lastName': 'testLastName',
                                                'pronouns': 'testPronouns',
                                                'isVirtual': True})

    # Validate
    assert response.status_code == 200
    assert json.loads(response.data)["user_id"] == 1

@patch('controller.user.authenticate')
@patch('data.users.exec_commit_return_autoincremented_id')
def test_post_user_with_error(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = None
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.post(User.PATH, json={'firstName': 'testFirstName',
                                                'lastName': 'testLastName',
                                                'pronouns': 'testPronouns',
                                                'isVirtual': True})

    # Validate
    assert response.status_code == 500

@patch('controller.user.authenticate')
@patch('data.users.exec_commit_return_autoincremented_id')
def test_post_user_with_missing_field(mock_db_exec, mock_authenticate, client):
    # mock object responses
    mock_db_exec.return_value = 1
    mock_authenticate.return_value = {"sub": "testAuth0ID"}

    # call endpoint
    response = client.post(User.PATH, json={'firstName': 'testFirstName',
                                                'pronouns': 'testPronouns',
                                                'isVirtual': True})

    # Validate
    assert response.status_code == 400
