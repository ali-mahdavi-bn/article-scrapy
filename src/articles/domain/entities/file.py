from datetime import datetime
from uuid import UUID, uuid4

from backbone.adapter.abstract_entity import BaseEntity


class File(BaseEntity):
    id: int
    uuid: UUID
    source: UUID
    path: str
    format: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, source: UUID, path: str, format: str, uuid: UUID = None):
        file = File()
        file.uuid = uuid or uuid4()
        file.source = source
        file.path = path
        file.format = format

        return file
