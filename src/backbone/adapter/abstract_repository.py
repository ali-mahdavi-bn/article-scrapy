from abc import ABC, abstractmethod
from typing import Set, Any
from uuid import UUID


class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()  # type: Set[Any]

    def add(self, model: any):
        self._add(model)
        self.seen.add(model)

    @abstractmethod
    def _add(self, model):
        raise NotImplementedError

    @property
    def soft_delete_field(self):
        return "deleted_at"

    def delete(self, model: any, soft_delete=True):
        self._delete(model, soft_delete)

    @abstractmethod
    def _delete(self, model, soft_delete: bool):
        raise NotImplementedError

    def find_by_id(self, identifier):
        data = self._find_by_id(identifier)
        if data:
            data.events = []
            self.seen.add(data)
        return data

    @abstractmethod
    def _find_by_id(self, identifier):
        raise NotImplementedError

    def find_by_uuid(self, identifier):
        data = self._find_by_uuid(identifier)
        if data:
            data.events = []
            self.seen.add(data)
        return data

    @abstractmethod
    def _find_by_uuid(self, identifier):
        raise NotImplementedError

    @abstractmethod
    def _find_by_uuid_and_org(self, identifier, organization_id):
        raise NotImplementedError

    def find_by_uuid_and_org(self, identifier: UUID, organization_id: UUID):
        data = self._find_by_uuid_and_org(identifier, organization_id)
        if data:
            data.events = []
            self.seen.add(data)
        return data
