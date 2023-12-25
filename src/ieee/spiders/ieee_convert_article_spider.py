import scrapy
from scrapy.http import HtmlResponse

from ieee.utils.generate_file_text import generate_file_text
from ieee.utils.get_item import fetch_article
from ieee.utils.get_proxy import get_proxy
from ieee.utils.request_args import RequestArgs
from ieee.utils.request_scrapy import request_scrapy
from ieee.utils.url import add_url_sci, find_url_pdf_sci
from unit_of_work import UnitOfWork


class IeeeConvertArticleSpider(scrapy.Spider):
    name = "ieee_convert_article_spider"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.file_text = ""

    def start_requests(self):
        page_number = 1
        articles = fetch_article(4, page_number)

        request_args = RequestArgs(parse=self.parse)
        if proxy := get_proxy():
            request_args.add_proxy(proxy)

        while articles:
            article = articles.pop(0)
            url = add_url_sci(url=article.link_article)
            request_args.add_url(url)
            request_args.add_meta(key="article", value=article)
            yield request_args.request_scrapy()

            if len(articles) == 0:
                page_number += 1
                articles += fetch_article(4, page_number)

    def parse(self, response: HtmlResponse):
        self._ieee_response = response
        self.article = response.meta["article"]
        yield self._parse_download_pdf_from_sci(response=response)

    def _parse_download_pdf_from_sci(self, response: HtmlResponse):
        url = find_url_pdf_sci(response=response)
        return request_scrapy(url=url, callback=self._save_pdf)

    def _save_pdf(self, response: HtmlResponse):
        article_text = generate_file_text(response=response)
        self._parse_detail(article_text=article_text)

    def _parse_detail(self, article_text: str):
        with UnitOfWork() as uow:
            article = uow.article.find_by_id(self.article.id)
            article.update(article, article_text, format="pdf")
            uow.commit()
            uow.session.refresh(article)

        uow.commit()
