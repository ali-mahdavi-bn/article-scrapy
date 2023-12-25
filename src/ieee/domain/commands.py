from typing import List, Optional
from uuid import UUID

from backbone.service_layer.general_types import Command


class RemoveActiveSession(Command):
    session_id: UUID
    token: str


class SendOtpCommand(Command):
    mobile: str


class RegisterUser(Command):
    mobile: str
    otp: str


class UpdateUserInfo(Command):
    user_id: UUID
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]


class UpdateUserName(Command):
    user_id: UUID
    username: str


class UpdateUserPassword(Command):
    password: str
    user_id: UUID


class GetAccessToken(Command):
    username: Optional[str] = ""
    password: Optional[str] = ""
    otp: Optional[str] = ""
    refresh_token: Optional[str] = ""
    code: Optional[str] = ""
    redirect_uri: Optional[str] = ""
    scope: str = "openid"
    client_id: Optional[str] = ""
    client_secret: Optional[str] = ""
    device_id: str
    ip: str
    captcha: Optional[str]

    def get_grant_type(self):
        grant_types = []
        if self.password != "":
            grant_types.append("password")
        if self.refresh_token != "":
            grant_types.append("refresh_token")
        if self.client_id != "" and self.client_secret != "":
            grant_types.append("client_credentials")
        if self.code != "":
            grant_types.append("authorization_code")

        return grant_types


class CheckPasswordCorrectness(Command):
    password: str
    username: str
    captcha: Optional[str]
    ip: str
    device_id: str


class UpdateUserTwoFactorAuth(Command):
    enable: bool
    user_id: UUID
