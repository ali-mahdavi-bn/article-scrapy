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
from unit_of_work import UnitOfWork


class IeeeArticleSpider(scrapy.Spider):
    name = "ieee_article_spider"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.file_text = ""

    def start_requests(self):
        urls = [
            #     f"https://ieeexplore.ieee.org/document/{i}"
            #     for i in range(6000000, 10300000)  # 99999999
            # "https://sci-hub.wf/https://ieeexplore.ieee.org/document/6292178"
            f"https://ieeexplore.ieee.org/document/{i}" for i in range(6292181, 6292190)
        ]

        request_args = RequestArgs(parse=self.parse)
        if proxy := get_proxy():
            request_args.add_proxy(proxy)

        for url in urls:
            request_args.add_url(url)
            yield request_args.request_scrapy()

    def parse(self, response: HtmlResponse):
        yield self._save_detail(response=response)

    def _save_detail(self, response: HtmlResponse):
        article_text = generate_file_text(response=response)
        detail_page_ieee = clear_data_ieee(response=response, article_text=article_text)
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
