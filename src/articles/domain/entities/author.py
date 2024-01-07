from datetime import datetime

from backbone.adapter.abstract_entity import BaseEntity


class Author(BaseEntity):
    id: int
    uuid: str
    first_name: str
    last_name: str
    affiliation: str
    authors_id: str
    bio: str
    created_at: datetime
    updated_at: datetime
