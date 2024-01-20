import time
from typing import Optional
from backbone.configs import config

from crawl.helper.helpers.response import Response


def find_url_pdf_sci(response: Response) -> Optional[str]:
    url = response.find('iframe', {'id': 'pdf'}).get("src")
    return url[:-10] if url else None


def add_url_sci(url: Response) -> str:
    return config.SCI_PATH + url
