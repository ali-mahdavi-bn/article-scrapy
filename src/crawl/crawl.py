import time

from crawl.backbone.helpers.response import Response
from crawl.backbone.adapter.abstract_crawl import AbstractCrawl
from utils.public.colors import color


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

    def start(self, spider):
        for request in spider().from_crawler():
            if not self._is_crawling:
                break
            self._run_flow(request=request)

    def start_supress_error(self, spider):
        for request in spider().from_crawler():
            if not self._is_crawling:
                break
            try:
                self._run_flow(request=request)
            except Exception as e:
                print(color.red(str(e)))

    def start_worker(self, spider, conditional_break=None, time_sleep_next_every_run=180):
        while True:
            if not self._is_crawling or (conditional_break and not conditional_break()):
                break

            try:
                for request in spider().from_crawler():
                    if not self._is_crawling:
                        break
                    if request:
                        self._run_flow(request=request)
                    # print("sleep time: ", time_sleep_next_every_run)
                    # time.sleep(time_sleep_next_every_run)
            except:
                pass
                # print("sleep time: ", time_sleep_next_every_run)
                # time.sleep(time_sleep_next_every_run)

    def stop(self):
        self._is_crawling = False
