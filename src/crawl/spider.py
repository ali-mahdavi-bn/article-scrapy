from typing import Any, Self

from crawl.helper.adapter.abstract_spider import AbstractSpider


class Spider(AbstractSpider):
    def start_requests(self, **kwargs) -> Self:
        raise NotImplementedError

    def from_crawler(self, crawler=None) -> Self:
        try:
            yield from self.start_requests()
        except Exception as e:
            print(str(e))
            yield []
