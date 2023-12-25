from typing import Callable, Optional, Any, Dict

import scrapy

from backbone.configs import config
from ieee.utils.request_scrapy import request_scrapy


class RequestArgs:
    def __init__(self, parse: Callable[[Any], Any], headers: Optional[Dict[str, str]] = None, url: str = None):
        self._request_args: dict = {"headers": headers} if headers else {"headers": config.DEFAULT_HEADERS}
        self._request_args["url"] = url if url else ""
        self._request_args["meta"] = {}
        self._parse: Callable[[Any], Any] = parse

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

    def request_scrapy(self) -> scrapy.Request:
        args: dict = self._request_args
        return request_scrapy(**args, callback=self._parse)
