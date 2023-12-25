from typing import Optional, Callable, Dict

import scrapy

from backbone.configs import config


def request_scrapy(url: str, callback: Callable, headers: Optional[Dict[str, str]] = None,
                   meta: Optional[Dict[str, str]] = None) -> scrapy.Request:
    """
    :param url:
    :param callback:
    :param headers:
    :param meta:
    :return: scrapy.Request
    """
    headers = headers or config.DEFAULT_HEADERS

    try:
        return scrapy.Request(url, headers=headers, callback=callback, meta=meta)
    except:
        try:
            return scrapy.Request("http:" + url, headers=headers, callback=callback, meta=meta)
        except:
            pass
