from typing import Callable, Optional, Dict

import requests

from backbone.configs import config
from src.utils.spider.request import request


class Request:
    def __init__(self, url, callback, headers=None, meta=None):
        self._meta = meta
        self._headers = headers or {}
        self._callback = callback
        self._url = url

    def get_url(self):
        return self._url

    def request(self):
        response = requests.get(self._url, headers=self._headers, timeout=2)
        return response


class RequestArgs:
    def __init__(self, callback: Callable, headers: Optional[Dict[str, str]] = None, url: str = None,
                 meta: dict = None):
        self._request_args: dict = {"headers": headers} if headers else {"headers": config.DEFAULT_HEADERS}
        self._request_args["url"] = url if url else ""
        self._request_args["meta"] = meta if meta else {}
        self.callback: Callable = callback

    def add_proxy(self, proxy: str) -> None:
        self._request_args["meta"]["proxy"] = proxy

    def add_meta(self, key, value):
        self._request_args["meta"][key] = value

    def add_header(self, headers: str) -> None:
        self._request_args["headers"] = {"headers": headers}

    def add_url(self, url: str) -> dict:
        self._request_args["url"] = url

    def get_arg(self) -> dict:
        return self._request_args

    def get_meta(self):
        return self._request_args["meta"]

    def get(self):
        args: dict = self._request_args
        return request(**args, callback=self.callback)
