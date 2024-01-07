from abc import ABC, abstractmethod


class CrawlImp(ABC):

    @abstractmethod
    def lifespan(self, lifespan):
        lifespan()

    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass
