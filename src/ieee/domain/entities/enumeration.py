from __future__ import annotations

from sqlalchemy import Column, Integer, String

from backbone.infrastructure.postgres_connection import BaseEntity


class Enumeration(BaseEntity):
    __tablename__ = "enumerations"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    parent_id = Column(Integer)

    @classmethod
    def create(cls, member):
        enum = Enumeration()
        enum.id = member.value
        enum.title = member.name
        enum.parent_id = member.parent()
        return enum
