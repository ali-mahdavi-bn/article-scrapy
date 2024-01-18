from articles.domain.commands import IeeeConvertArticle
from articles.spider.ieee_convert_article_spider import IeeeConvertArticleSpider
from crawl.crawl import Crawler


def ieee_article_convert_handler(command: IeeeConvertArticle):
    crw = Crawler()
    crw.start_worker(IeeeConvertArticleSpider)
