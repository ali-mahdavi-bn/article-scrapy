import random
import datetime

import sentry_sdk
from kavenegar import *

from account.domain.entities import OtpCode
from backbone.configs import config
from backbone.infrastructure.log.logger import LoggerFactory
from enumeration.domain.enums import OtpStatus
from unit_of_work import UnitOfWork

EXPIRED_TIME = 120  # second


class OtpError(Exception):
    pass


class OtpService:
    LOGGER = LoggerFactory.get_logger("OtpService")

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.is_created_new_otp = False
        self.LOGGER = LoggerFactory.get_logger(self.__class__)

    def verify_otp(self, mobile, code) -> OtpCode:
        otp = self.uow.otp_code.find_by_mobile(mobile)
        if otp and str(otp.code) == code and self._time_left(otp) > 0:
            otp.update_status(OtpStatus.VERIFIED)
            return otp
        raise OtpError("incorrect otp")

    @classmethod
    def _time_left(cls, obj) -> int:
        now = datetime.datetime.now()
        interval = now - obj.created_at.replace(tzinfo=None)
        return int(EXPIRED_TIME - interval.total_seconds())

    def create(self, mobile) -> OtpCode and int:
        obj = self.uow.otp_code.find_by_mobile(mobile)
        self.is_created_new_otp = False
        if obj:
            time_left = self._time_left(obj)
            if time_left > 0:
                return obj, time_left
            else:
                obj.update_status(OtpStatus.DEPRECATED)

        self.is_created_new_otp = True
        return self._create(mobile), EXPIRED_TIME

    def _create(self, mobile: str) -> OtpCode:
        code = str(random.randint(100000, 999999))
        obj = OtpCode()
        obj.code = code
        obj.mobile = mobile
        obj.status = OtpStatus.CREATED.value
        obj.created_at = datetime.datetime.now()
        self.uow.otp_code.add(obj)
        return obj

    @classmethod
    def send(cls, otp: OtpCode):
        # todo : send to automation
        try:

            # این خط حقیر خدماتی است و به همه پیامک میره
            # باشد که در دمو کف همه ببرّد
            api = KavenegarAPI(config.KAVENEGAR_ACCESS_KEY)
            params = {
                'receptor': otp.mobile,
                'sender': 90005801,
                'message': f"code {otp.code} \n کد ورود به هولدینگ تایمز \n timez.ir",

            }
            response = api.sms_send(params)
            #
            # api = KavenegarAPI('70544A3264624F757569322B31356144464C34364D4F3643722F6C33416A3243')
            # params = {
            #     'receptor': otp.mobile,
            #     'template': 'loginOTP',
            #     'token': otp.code,
            #     'type': 'sms',  # sms vs call
            # }
            # response = api.verify_lookup(params)
            # cls.update_status(otp, OtpStatus.SEND_TO_USER)
        except APIException as e:
            sentry_sdk.capture_exception(e)
            cls.LOGGER.exception(e)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            cls.LOGGER.exception(e)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            cls.LOGGER.exception(e)
