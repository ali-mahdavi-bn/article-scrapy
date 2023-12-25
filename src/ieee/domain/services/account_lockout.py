from backbone.service_layer.abstract_cache import AbstractStore


class AccountLockout:

    def __init__(self, cache: AbstractStore):
        self.cache_provider = cache

    def is_blocked(self, ip, device_id, mobile=None):
        keys = {"ip": ip, "device_id": device_id}
        if mobile:
            keys["mobile"] = mobile
        for k, value in keys.items():
            block_key = f"login:suspend:{k}:{value}"
            if self.cache_provider.get_value(block_key):
                return True

    def login_attempt_filed(self, ip, device_id, mobile=None):
        keys = {"ip": ip, "device_id": device_id}
        if mobile:
            keys["mobile"] = mobile
        for k, value in keys.items():
            item_key = f"throttle:login:{k}:{value}"
            count = self.cache_provider.get_value(item_key)
            count = int(count) + 1 if count else 1
            if count >= 10:
                block_key = f"login:suspend:{k}:{value}"
                self.cache_provider.set_value(key=block_key, value="True", exp=60*10)
            self.cache_provider.set_value(key=item_key, value=count, exp=120)

    def login_attempt_success(self, ip, device_id, mobile=None):
        keys = {"ip": ip, "device_id": device_id}
        if mobile:
            keys["mobile"] = mobile
        for k, value in keys.items():
            block_key = f"login:suspend:{k}:{value}"
            self.cache_provider.delete_key(block_key)
