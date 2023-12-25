from account.domain import commands
from account.domain.services.account_lockout import AccountLockout
from account.domain.services.captcha import CaptchaService
from backbone.exception import NotFoundException
from backbone.infrastructure.microservices.auth import AuthMicroservice
from backbone.service_layer.abstract_cache import AbstractStore
from unit_of_work import UnitOfWork


def check_password_correctness_handler(command: commands.CheckPasswordCorrectness, auth_servie: AuthMicroservice,
                                       store: AbstractStore, uow: UnitOfWork):
    lockout = AccountLockout(store)
    CaptchaService(store=store, lockout_service=lockout).verify(ip=command.ip, device_id=command.device_id,
                                                                mobile=command.username,
                                                                captcha=command.captcha)
    with uow:
        user = uow.user.find_by_mobile(command.username)
        if not user:
            raise NotFoundException("User.NotFound")
        result = {"result": True,
                  "two_factor_authenticate": user.two_factor_authentication if user.two_factor_authentication else False}
        try:
            auth_servie.openid().token(username=command.username, password=command.password)
            lockout.login_attempt_success(ip=command.ip, device_id=command.device_id, mobile=command.username)
        except Exception:
            lockout.login_attempt_filed(mobile=command.username, ip=command.ip, device_id=command.device_id)
            result["result"] = False

        return result
