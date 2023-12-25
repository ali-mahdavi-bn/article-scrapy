from account.domain import commands
from account.domain.services.otp import OtpError
from account.domain.services.user_register import RegisterUserService
from backbone.infrastructure.microservices.auth import AuthMicroservice
from unit_of_work import UnitOfWork
from backbone.exception.http_exception.exceptions import BadRequestException


def register_user(command: commands.RegisterUser, uow: UnitOfWork, auth_servie: AuthMicroservice):
    with uow:
        try:
            register_service = RegisterUserService(uow, auth_servie)
            register_service.register(mobile=command.mobile, otp_code=command.otp)
            uow.commit()
            return register_service.token
        except OtpError:
            raise BadRequestException("your otp is deprecated or wrong.")
