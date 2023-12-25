from fast_captcha import img_captcha

from account.domain.services.account_lockout import AccountLockout
from backbone.exception.logical_validation_exeption.exeptions import LogicalValidationException
from backbone.service_layer.abstract_cache import AbstractStore


class CaptchaService:
    def __init__(self, store: AbstractStore, lockout_service=None):
        self.key = "captcha:{device_id}:{ip}:{mobile}"
        self.store = store
        if not lockout_service:
            self.lockout_service = AccountLockout(store)
        else:
            self.lockout_service = lockout_service

    def get_captcha(self, ip, device_id, mobile=None):
        img, text = img_captcha()
        self.store.set_value(key=self.key.format(ip=ip, device_id=device_id, mobile=mobile), value=text,
                             exp=3 * 60)
        return img

    def is_valid(self, captcha_text, ip, device_id, mobile=None):
        text = self.store.get_value(key=self.key.format(ip=ip, device_id=device_id, mobile=mobile))
        if not text or text.decode().lower() != captcha_text.lower():
            raise LogicalValidationException(
                message="validation.wrong_or_deprecated_captcha",
                type_="wrong_or_deprecated_captcha",
                location="body.captcha"
            )
        return True

    def verify(self, captcha, ip, device_id, mobile=None):
        return True
        if self.lockout_service.is_blocked(mobile=mobile, ip=ip, device_id=device_id):
            if captcha:
                self.is_valid(captcha_text=captcha, ip=ip, device_id=device_id,
                              mobile=mobile)
                self.store.delete_key(key=self.key.format(ip=ip, device_id=device_id, mobile=mobile))
            else:
                raise LogicalValidationException(message="validation.captcha_needed", type_="captcha_needed",
                                                 location="body.captcha")
