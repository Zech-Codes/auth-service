from auth.app import app
from auth.models.status import Status, StatusResponse
from auth.models.user import User
from auth.templating import render
from enum import Enum
from pydantic import BaseModel


class AuthenticationType(Enum):
    EMAIL = "EMAIL"
    USERNAME = "USERNAME"


class UserAuthentication(BaseModel):
    user: str
    auth_type: AuthenticationType
    redirect: str


@app.post("/v1/authenticate")
async def authenticate(auth_details: UserAuthentication) -> StatusResponse:
    func_map = {
        AuthenticationType.EMAIL: User.get_user_by_email,
        AuthenticationType.USERNAME: User.get_user
    }
    user = func_map[auth_details.auth_type](auth_details.user)
    if user:
        message = render(
            "emails/login.html",
            username=user.username,
            login_link=auth_details.redirect
        )
        send_email(user.email, message)
    return StatusResponse(status=Status.SUCCESS)


def send_email(address, message):
    print("\n****** Hi ******")
    print(address)
    print(message)
    print("******")
