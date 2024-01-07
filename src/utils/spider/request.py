from typing import Optional, Callable, Dict


from backbone.configs import config


def request(url: str, callback: Callable, headers: Optional[Dict[str, str]] = None,
                   meta: Optional[Dict[str, str]] = None):
    """
    :param url:
    :param callback:
    :param headers:
    :param meta:
    :return: scrapy.Request
    """
    from src.crawl.backbon.helpers.requests import Request

    headers = headers or config.DEFAULT_HEADERS

    try:
        req = Request(url=url, callback=callback, headers=headers, meta=meta)
        return req.request()
    except:
        try:
            req = Request(url="http:" + url, callback=callback, headers=headers, meta=meta)
            return req.request()
        except Exception as e:
            raise e

