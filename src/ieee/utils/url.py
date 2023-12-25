from typing import Optional
from backbone.configs import config
from scrapy.http import HtmlResponse


def find_url_pdf_sci(response: HtmlResponse) -> Optional[str]:
    url = response.css("div#article > #pdf::attr(src)").get()
    return url[:-10] if url else None


def add_url_sci(url: HtmlResponse) -> str:
    return config.SCI_PATH + url
