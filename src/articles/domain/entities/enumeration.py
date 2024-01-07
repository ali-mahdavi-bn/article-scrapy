from __future__ import annotations

from backbone.adapter.abstract_entity import BaseEntity


class Enumeration(BaseEntity):
    __tablename__ = "enumerations"
    id: int
    title: str
    parent_id: int

    @classmethod
    def create(cls, member):
        enum = Enumeration()
        enum.id = member.value
        enum.title = member.name
        enum.parent_id = member.parent()
        return enum
