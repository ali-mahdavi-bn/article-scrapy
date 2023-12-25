from account.domain import commands
from account.domain.services.account_lockout import AccountLockout
from account.domain.services.captcha import CaptchaService
from account.domain.services.otp import OtpError
from account.domain.services.user_register import RegisterUserService
from backbone.exception import UnauthorizedException, BadRequestException
from backbone.exception.logical_validation_exeption.exeptions import LogicalValidationException
from backbone.helpers.utils import remove_none_from_dict
from backbone.infrastructure.log.logger import LoggerFactory
from backbone.infrastructure.microservices.auth import AuthMicroservice
from backbone.service_layer.abstract_cache import AbstractStore
from unit_of_work import UnitOfWork

logger = LoggerFactory.get_logger(__name__)


def get_access_token(command: commands.GetAccessToken, uow: UnitOfWork, auth_servie: AuthMicroservice,
                     store: AbstractStore):
    lockout = AccountLockout(store)
    CaptchaService(store=store, lockout_service=lockout).verify(ip=command.ip, device_id=command.device_id,
                                                                mobile=command.username, captcha=command.captcha)
    with uow:
        try:
            user = uow.user.find_by_mobile(command.username)
            register_service = RegisterUserService(uow, auth_servie)
            if not command.code:
                # create user if not exist
                if not user:
                    register_service.register(mobile=command.username, otp_code=command.otp)
                    uow.commit()
                    return register_service.token

                # reset password
                if command.otp and not command.password:
                    register_service.login_with_otp(user=user, otp_code=command.otp)
                    return register_service.token

                # two_factor_authentication
                if user.two_factor_authentication:
                    register_service.two_factor_login(user=user, password=command.password, otp_code=command.otp)
                    return register_service.token

            payload = remove_none_from_dict(command.dict(), remove_empty_string=True)
            payload["grant_type"] = command.get_grant_type()
            token = AuthMicroservice().openid().token(**payload)
            lockout.login_attempt_success(ip=command.ip, device_id=command.device_id, mobile=command.username)
            return token
        except OtpError:
            lockout.login_attempt_filed(mobile=command.username, ip=command.ip, device_id=command.device_id)
            raise BadRequestException("your otp is deprecated or wrong.")
        except Exception as e:
            logger.exception(e)
            lockout.login_attempt_filed(mobile=command.username, ip=command.ip, device_id=command.device_id)
            raise UnauthorizedException()
