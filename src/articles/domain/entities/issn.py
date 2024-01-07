from datetime import datetime
from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity


class Issn(BaseEntity):

    id: int
    format: str
    keyword: str
    article_id: UUID
    created_at: datetime
    updated_at: datetime
