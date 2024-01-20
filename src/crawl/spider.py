from typing import Any, Self

from crawl.helper.adapter.abstract_spider import AbstractSpider


class Spider(AbstractSpider):
    def start_requests(self, **kwargs) -> Self:
        raise NotImplementedError

    def from_crawler(self, crawler=None) -> Self:
        yield from self.start_requests()
