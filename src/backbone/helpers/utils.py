import datetime
from inspect import getmembers, isfunction, signature, isclass
from types import NoneType
from typing import Dict, Type, Any, Callable, List

from dateutil.parser import parse
from fastapi import FastAPI


def remove_none_from_dict(dictionary: dict, remove_empty_string=False):
    for key, value in list(dictionary.items()):
        if value is None:
            del dictionary[key]
        if remove_empty_string and isinstance(value, str) and value == "":
            del dictionary[key]
        elif isinstance(value, dict):
            remove_none_from_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    remove_none_from_dict(item)

    return dictionary


def datetime_to_str(time: datetime.datetime) -> str:
    return time.strftime('%Y/%m/%dT%H:%M:%S')


def collect_handlers_functions(module) -> Dict[Any, Callable | List[Callable]]:
    functions = {}  # type: Dict[Any, Callable| List[Callable]]
    for p, c in getmembers(module, isfunction):
        for name, model_type in signature(c).parameters.items():
            if name == "command":
                functions.update({model_type.annotation: c})
                break

            if name == "message":
                functions.setdefault(model_type.annotation, []).append(c)
                break

    return functions


def install_module(app: FastAPI, module):
    for name, c in getmembers(module):
        if name == "start_mapper":
            c()
        if name.startswith("router"):
            app.include_router(c)


def any_to_datetime(date_or_datetime):
    if type(date_or_datetime) == str:
        _datetime = parse(date_or_datetime)
    elif type(date_or_datetime) == datetime.date:
        _datetime = datetime.datetime(date_or_datetime.year, date_or_datetime.month, date_or_datetime.day)
    else:
        _datetime = date_or_datetime

    return _datetime


class TimeOperation:
    @classmethod
    def is_equal(cls, t1, t2):
        if isinstance(t1.utcoffset(), NoneType) and isinstance(t2.utcoffset(), NoneType):
            return t1 == t2
        time1 = (datetime.datetime.combine(datetime.datetime.today(), t1) - t1.utcoffset()).time()
        time2 = (datetime.datetime.combine(datetime.datetime.today(), t2) - t2.utcoffset()).time()
        return time1 == time2

    @classmethod
    def minus_times(cls, t1: datetime.time, t2: datetime.time):
        time1 = (datetime.datetime.combine(datetime.datetime.today(), t1) - t1.utcoffset()).time()
        time2 = (datetime.datetime.combine(datetime.datetime.today(), t2) - t2.utcoffset()).time()
        delta = datetime.datetime.combine(datetime.datetime.today(), time2) - datetime.datetime.combine(
            datetime.datetime.today(), time1)
        return delta
