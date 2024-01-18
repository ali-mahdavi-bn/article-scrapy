from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel

from backbone.helpers.validation import PhoneNumberValidator, PostalCodeValidator


class BaseEnumeration(Enum):
    @classmethod
    def members(cls) -> List[BaseEnumeration]:
        return [item[1] for item in cls.__members__.items()]




    @classmethod
    def find_by_value(cls, value) -> BaseEnumeration:
        for item in cls.members():
            if value == item.value:
                return item


class Command(BaseModel):
    pass

class Event(BaseModel):
    pass


class ValueObject(BaseModel):
    pass


class PrimitiveType(Enum):
    INT = "int"
    FLOAT = "float"
    DATETIME = "date_time"
    DATE = "date"
    STRING = "string"
    UUID = "uuid"


class PhoneNumber(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any):
        PhoneNumberValidator("body.phone_number", value).validate()
        return cls


class PostalCode(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any):
        PostalCodeValidator("body.postal_code", value).validate()
        return cls


@dataclasses.dataclass
class Name:
    first_name: Optional[str]
    last_name: Optional[str]

    # Sqlalchemy composite callback func
    def __composite_values__(self):
        return self.first_name, self.last_name

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
