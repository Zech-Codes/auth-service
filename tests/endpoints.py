from auth import app
from fastapi.testclient import TestClient
from pytest import fixture
from pytest_mock import mocker
import auth.authenticate
import auth.database
import auth.models.user


client = TestClient(app)


@fixture(scope="function")
def database(mocker):
    mocker.patch.object(auth.database.Database, "connect")
    mocker.patch.object(auth.database.Database, "session")


@fixture(scope="function")
def send_email(mocker):
    return mocker.patch.object(auth.authenticate, "send_email")


@fixture(scope="function")
def get_user(mocker):
    user = auth.models.user.User(
        username="johndoe",
        email="johndoe@email.com",
        ID=0
    )
    by_email = mocker.patch.object(auth.models.user.User, "get_user_by_email")
    by_id = mocker.patch.object(auth.models.user.User, "get_user_by_id")
    by_name = mocker.patch.object(auth.models.user.User, "get_user")
    by_email.return_value = user
    by_id.return_value = user
    by_name.return_value = user


@fixture(scope="function")
def render_template(mocker):
    return mocker.patch.object(auth.authenticate, "render")


def test_authentication_success(send_email, database, render_template):
    response = client.post(
        "/v1/authenticate",
        json={
            "user": "johndoe@email.com",
            "auth_type": "EMAIL",
            "redirect": "http://localhost:8081/authenticate/"
        }
    )
    assert response.json().get("status") == "SUCCESS"


def test_authentication_email_sent(send_email, get_user, render_template):
    response = client.post(
        "/v1/authenticate",
        json={
            "user": "johndoe@email.com",
            "auth_type": "EMAIL",
            "redirect": "http://localhost:8081/authenticate/"
        }
    )
    render_template.assert_called_once_with(
        "emails/login.html",
        username="johndoe",
        login_link="http://localhost:8081/authenticate/"
    )
    send_email.assert_called_once_with("johndoe@email.com", render_template())
