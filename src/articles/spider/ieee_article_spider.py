from articles.domain.entities import Article
from articles.spider.utils.clear_data import clear_data_ieee
from crawl.helper.helpers.requests import RequestArgs
from crawl.helper.helpers.response import Response
from crawl.spider import Spider
from unit_of_work import UnitOfWork
from utils.public.articles import create_article_and_dependencies


class IeeeArticleSpider(Spider):
    name = "ieee_article_spider"

    def __init__(self):
        super().__init__()
        self.file_text = ""
        self.is_get_max_id_article = False

    def start_requests(self, **kwargs):
        request_args = RequestArgs(callback=self.parse)
        max_id_article_in_db = self._get_max_id_article_in_db()
        min_article_id = int(max_id_article_in_db) if max_id_article_in_db else 6000306
        max_article_id = 10388489

        for item in range(min_article_id, max_article_id):
            url = f"https://ieeexplore.ieee.org/document/{item}"
            request_args.add_url(url)
            yield request_args

    def parse(self, response: Response):
        self._save_detail(response=response)

    def _save_detail(self, response: Response):
        detail_page_ieee = clear_data_ieee(response=response)

        create_article_and_dependencies(detail_page_ieee)

    def _get_max_id_article_in_db(self):
        with UnitOfWork() as uow:
            max_id_article: Article = uow.session.query(Article).filter(Article.publisher == "IEEE").order_by(
                Article.article_id.desc()).first()
        return max_id_article.article_id if max_id_article else None
