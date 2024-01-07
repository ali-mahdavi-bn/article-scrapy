from articles.domain.mapper import start_mapper
from articles.spider.utils.clear_data import clear_data_ieee
from articles.spider.utils.get_proxy import get_proxy
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN
from crawl.backbon.helpers.requests import RequestArgs
from crawl.backbon.helpers.response import Response
from crawl.crawl import Crawler
from crawl.spider import Spider
from src.utils.articles import create_article_and_dependencies


class Aaaa: pass


class IeeeArticleSpider(Spider):
    name = "ieee_article_spider"

    def __init__(self):
        super().__init__()
        self.file_text = ""


    def start_requests(self):
        urls = [
            f"https://ieeexplore.ieee.org/document/{i}" for i in range(6292181, 6292190)
        ]

        request_args = RequestArgs(callback=self.parse)
        if proxy := get_proxy():
            request_args.add_proxy(proxy)

        for url in urls:
            request_args.add_url(url)
            yield request_args

    def parse(self, response: Response):
        self._save_detail(response=response)

    def _save_detail(self, response: Response):
        detail_page_ieee = clear_data_ieee(response=response)

        create_article_and_dependencies(detail_page_ieee)
def lifspan():
    start_mapper()
    MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)


crw = Crawler(lifespan=lifspan)
crw.start_iso(IeeeArticleSpider)