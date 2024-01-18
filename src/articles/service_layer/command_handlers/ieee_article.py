from articles.domain.commands import IeeeArticle
from articles.spider.ieee_article_spider import IeeeArticleSpider
from crawl.crawl import Crawler


def ieee_article_handler(command: IeeeArticle):
    crw = Crawler()
    crw.start_worker(IeeeArticleSpider)

