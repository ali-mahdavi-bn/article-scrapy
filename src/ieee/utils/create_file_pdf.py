from typing import Tuple
from datetime import datetime
from backbone.configs import config
from scrapy.http import HtmlResponse


def create_file_pdf(response: HtmlResponse, filename: str) -> str:
    with open(config.PDF_WEB + filename + ".pdf", "wb") as f:
        f.write(response.body)
    return filename


def generate_file_name_with_url(response: HtmlResponse) -> str:
    return response.url.split("/")[-1] + "_" + str(datetime.now())
