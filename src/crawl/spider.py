from typing import Any, Self

from crawl.backbon.service_layer.abstract_spider import SpiderImp


class Spider(SpiderImp):
    def from_crawler(self, crawler=None, *args: Any, **kwargs: Any) -> Self:
        yield from self.start_requests()
