from typing import Optional
from uuid import UUID

from backbone.service_layer.general_types import Event, Name


class UserCreated(Event):
    mobile: str
    name: Optional[Name] = None
    email: str = None


class LoginFailed(Event):
    mobile: str
    ip: str
    device_id: str
