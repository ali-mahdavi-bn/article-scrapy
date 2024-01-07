from abc import ABC, abstractmethod
from typing import Any, Self


class SpiderImp(ABC):
    @abstractmethod
    def from_crawler(self, crawler=None, *args: Any, **kwargs: Any) -> Self: pass

