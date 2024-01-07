from articles.domain.mapper import start_mapper
from articles.spider.utils.file import generate_file_text
from articles.spider.utils.get_item import fetch_article_empty_article_text
from articles.spider.utils.url import add_url_sci, find_url_pdf_sci
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN
from crawl.backbon.helpers.requests import RequestArgs
from crawl.backbon.helpers.response import Response
from crawl.crawl import Crawler
from crawl.spider import Spider
from unit_of_work import UnitOfWork


class IeeeConvertArticleSpider(Spider):
    name = "ieee_convert_article_spider"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.file_text = ""

    def start_requests(self):
        page_number = 1
        print("aaaaaa")
        while True:
            articles = fetch_article_empty_article_text(3, page_number)
            if not articles:
                break

            for article in articles:
                url = add_url_sci(url=article.link_article)
                request = RequestArgs(
                    url=url,
                    callback=self.parse,
                    meta={'articles': article}
                )
                yield request

    def parse(self, response: Response):
        self._ieee_response = response
        self.article = response.meta["articles"]
        yield self._parse_download_pdf_from_sci(response=response)

    def _parse_download_pdf_from_sci(self, response: Response):
        url = find_url_pdf_sci(response=response)
        return RequestArgs(url=url, callback=self._save_pdf)

    def _save_pdf(self, response: Response):
        print(self.article.id)
        article_text = generate_file_text(response=response)
        self._parse_detail(article_text=article_text)

    def _parse_detail(self, article_text: str):
        with UnitOfWork() as uow:
            article = uow.article.find_by_id(self.article.id)
            article.update_article_text(article_text)
            uow.commit()
            uow.session.refresh(article)

        uow.commit()


def lifspan():
    start_mapper()
    MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)


crw = Crawler(lifespan=lifspan)
crw.start_iso(IeeeConvertArticleSpider)
