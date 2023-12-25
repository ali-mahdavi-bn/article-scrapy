from abc import ABC, abstractmethod
from typing import Generic

from neo4j import Transaction

from backbone.adapter.abstract_sqlalchemy_repository import ENTITY


class AbstractNeo4jRepository(ABC, Generic[ENTITY]):
    pass
