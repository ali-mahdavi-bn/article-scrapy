from account.domain.entities.user import User
from account.domain.services.otp import OtpService
from backbone.infrastructure.microservices.auth import AuthMicroservice
from unit_of_work import UnitOfWork


class RegistrationException(Exception):
    pass


class RegisterUserService:
    def __init__(self, uow: UnitOfWork, auth_servie: AuthMicroservice):
        self.uow = uow
        self.auth_servie = auth_servie
        self._otp_service = OtpService(uow)
        self.user: User = User()
        self.token: dict = {}

    def mobile_has_registered(self, mobile: str) -> bool:
        user = self.uow.user.find_by_mobile(mobile)
        if user:
            return True

    def login_with_otp(self, user, otp_code: str):
        otp = self._otp_service.verify_otp(mobile=user.mobile, code=otp_code)
        user_uuid = user.uuid.__str__()
        self.auth_servie.remove_user_credential(user_uuid)
        self.auth_servie.get_admin_keycloak_openid().set_user_password(user_uuid, password=otp.code,
                                                                       temporary=False)
        self.token = self.auth_servie.openid().token(username=user.mobile, password=otp.code)
        self.auth_servie.remove_user_credential(user_uuid)

    def two_factor_login(self, user, password, otp_code):
        self._otp_service.verify_otp(mobile=user.mobile, code=otp_code)
        self.token = self.auth_servie.openid().token(username=user.mobile, password=password)

    def register(self, mobile: str, otp_code: str):
        if self.mobile_has_registered(mobile):
            raise RegistrationException("You have already registered.")

        otp = self._otp_service.verify_otp(mobile=mobile, code=otp_code)

        keycloak_users_id = self.auth_servie.get_admin_keycloak_openid().create_user({
            "username": mobile, "enabled": True}, exist_ok=True)

        self.auth_servie.remove_user_credential(keycloak_users_id)
        self.auth_servie.get_admin_keycloak_openid().set_user_password(keycloak_users_id, password=otp.code,
                                                                       temporary=False)
        user = User()
        user.mobile = mobile
        user.uuid = keycloak_users_id
        self.user = self.uow.user.add(user)

        self.token = self.auth_servie.openid().token(username=mobile, password=otp.code)
        self.auth_servie.remove_user_credential(keycloak_users_id)
