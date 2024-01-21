from articles.spider.utils.file import generate_file_text
from articles.spider.utils.get_item import fetch_article_empty_article_text
from articles.spider.utils.url import add_url_sci, find_url_pdf_sci
from crawl.helper.helpers.requests import RequestArgs
from crawl.helper.helpers.response import Response
from crawl.spider import Spider
from unit_of_work import UnitOfWork


class IeeeConvertArticleSpider(Spider):
    name = "ieee_convert_article_spider"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.file_text = ""

    def start_requests(self, **kwargs):

        page_size = 3
        page_number = 1
        while True:
            articles = fetch_article_empty_article_text(page_size, page_number)
            if not articles:
                break

            request = RequestArgs(
                callback=self.parse,
            )

            request.add_proxy("4c79f152-ef9f-421c-b0c1-3f6cb4c3b8cd.hsvc.ir:31633")
            for article in articles:
                url = add_url_sci(url=article.link_article)
                request.add_url(url)

                request.add_meta('articles', article)
                yield request

    def parse(self, response: Response):
        self._ieee_response = response
        self.article = response.meta["articles"]
        yield self._download_pdf_from_sci(response=response)

    def _download_pdf_from_sci(self, response: Response):
        url = find_url_pdf_sci(response=response)
        return RequestArgs(url=url, callback=self.generate_text)

    def generate_text(self, response: Response):
        article_text = generate_file_text(response=response)
        self._save_aticle_text(article_text=article_text)

    def _save_aticle_text(self, article_text: str):
        with UnitOfWork() as uow:
            article = uow.article.find_by_id(self.article.id)
            article.update_article_text(article_text)
            uow.commit()
            uow.session.refresh(article)
            uow.commit()
