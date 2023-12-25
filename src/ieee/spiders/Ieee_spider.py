import scrapy
from scrapy.http import HtmlResponse

from ieee.domain.command import PaperData
from ieee.domain.entities import ArticleEntity
from ieee.domain.services.make_list_authors import make_list_authors
from ieee.domain.services.make_list_issn import make_list_issn
from ieee.domain.services.make_list_keyword import make_list_keyword
from ieee.utils.clear_data import clear_data_ieee
from ieee.utils.generate_file_text import generate_file_text
from ieee.utils.get_proxy import get_proxy
from ieee.utils.request_args import RequestArgs
from ieee.utils.request_scrapy import request_scrapy
from ieee.utils.url import find_url_pdf_sci, add_url_sci
from unit_of_work import UnitOfWork


class IeeeSpider(scrapy.Spider):
    name = "detail_ieee"

    def start_requests(self):
        url = "https://ieeexplore.ieee.org/document/10333123"

        request_args = RequestArgs(parse=self.parse)

        if proxy := get_proxy():
            request_args.add_proxy(proxy)

        request_args.add_url(url)
        yield request_args.request_scrapy()

    def parse(self, response: HtmlResponse):
        self._ieee_response = response
        yield self._parse_download_pdf(response=response)

    def _parse_download_pdf(self, response: HtmlResponse):
        url = add_url_sci(url=response.url)
        return request_scrapy(url=url, callback=self._parse_download_pdf_from_sci)

    def _parse_download_pdf_from_sci(self, response: HtmlResponse):
        url = find_url_pdf_sci(response=response)
        return request_scrapy(url=url, callback=self._save_pdf)

    def _save_pdf(self, response: HtmlResponse):
        article_text = generate_file_text(response=response)
        self._parse_detail(article_text=article_text)

    def _parse_detail(self, article_text: str):
        detail_page_ieee = clear_data_ieee(self._ieee_response, article_text=article_text)
        list_bulk_object = []
        with UnitOfWork() as uow:
            authors = make_list_authors(detail_page_ieee, uow)
            issn = make_list_issn(detail_page_ieee)
            keyword = make_list_keyword(detail_page_ieee)

            list_bulk_object.extend(authors)
            list_bulk_object.extend(issn)
            list_bulk_object.extend(keyword)

            cleared_detail_page_ieee = PaperData.create(detail_page_ieee, authors=authors)
            author = ArticleEntity.create(cleared_detail_page_ieee,
                                          format="pdf")

            list_bulk_object.append(author)
            uow.session.add_all(list_bulk_object)

            uow.commit()
