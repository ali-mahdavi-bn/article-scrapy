from backbone.service_layer.general_types import BaseEnumeration


class KeyWordType(BaseEnumeration):
    IEEE_Keywords = 1011

    @classmethod
    def parent(cls):
        return 1010

class KeyWordjType(BaseEnumeration):
    IEEE_Keywords = 1020

    @classmethod
    def parent(cls):
        return 1021
