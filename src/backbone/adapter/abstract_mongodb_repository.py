from abc import ABC, abstractmethod

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from backbone.adapter.abstract_repository import AbstractRepository
from backbone.configs import config


class AbstractMongoDbRepository(ABC):

    def __init__(self, session: ClientSession):
        self.session = session

    @abstractmethod
    @property
    def collection_name(self) -> str:
        raise NotImplementedError

    @property
    def collection(self) -> Collection:
        return self.session.client[config.MONGODB_DATABASE][self.collection_name]
