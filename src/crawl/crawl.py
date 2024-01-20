import time

from backbone.infrastructure.log._logger import Logger
from crawl.helper.adapter.abstract_crawl import AbstractCrawl
from crawl.helper.helpers.response import Response


class Crawler(AbstractCrawl):


    def __init__(self, lifespan=None):
        (self._lifespan(lifespan)) if lifespan else None

        self._is_crawling = True

    def _lifespan(self, lifespan):
        lifespan()

    def _run_flow(self, request):
        content = Response(request=request)
        next_flow = request.callback(content)
        if next_flow:
            for nf in next_flow:
                self._run_flow(request=nf)

    def start(self, spider, conditional_break=None):
        Logger.info(f"starting spider {spider.__name__}")
        for request in spider().from_crawler():
            if conditional_break and not conditional_break():
                Logger.info("spider break")
                break
            self._run_flow(request=request)

    def start_supress_error(self, spider, conditional_break=None):
        Logger.info(f"starting spider {spider.__name__}")

        for request in spider().from_crawler():
            if conditional_break and not conditional_break():
                Logger.info("spider break")
                break
            try:
                self._run_flow(request=request)
            except Exception as e:
                Logger.info(f"Spider Error: {e}")

    def start_worker(self, spider, conditional_break=None, time_sleep_next_every_run=180):
        while True:
            Logger.info("worker running...")
            if conditional_break and not conditional_break():
                Logger.info("worker break...")
                break

            try:
                Logger.info(f"execute spider {spider.__name__}")
                for request in spider().from_crawler():
                    if request:
                        self._run_flow(request=request)
                    time.sleep(time_sleep_next_every_run)
            except Exception as e:
                Logger.info(f"Worker Error: {e}")
                time.sleep(time_sleep_next_every_run)
