from crawl.backbon.helpers.response import Response
from crawl.backbon.service_layer.abstract_crawl import CrawlImp
from src.utils.public.colors import color


class Crawler(CrawlImp):

    def __init__(self, lifespan=None):
        (self.lifespan(lifespan)) if lifespan else None

        self._process = True

    def lifespan(self, lifespan):
        lifespan()

    def _run_flow(self, request):
        content = Response(request=request)
        next_flow = request.callback(content)
        if next_flow:
            for nf in next_flow:
                self._run_flow(request=nf)

    def start(self, spiders):
        for request in spiders().from_crawler():
            if not self._process:
                break
            self._run_flow(request=request)

    def start_iso(self, spiders):
        for request in spiders().from_crawler():
            if not self._process:
                break
            try:
                self._run_flow(request=request)
            except Exception as e:
                print(color.red(str(e)))

    def start_worker(self, spiders, conditional_break=None):
        while True:
            if not self._process or (conditional_break and not conditional_break()):
                break

            try:
                for request in spiders().from_crawler():
                    if not self._process:
                        break

                    self._run_flow(request=request)
            except:
                pass

    def stop(self):
        self._process = False
