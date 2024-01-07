from datetime import datetime

from backbone.adapter.abstract_entity import BaseEntity


class Keyword(BaseEntity):

    id: int
    type: str
    keyword: str
    article_id: int
    created_at: datetime
    updated_at: datetime
