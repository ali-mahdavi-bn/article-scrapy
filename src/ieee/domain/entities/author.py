from sqlalchemy import Integer, Column, String, DateTime, func, Text, Uuid
from sqlalchemy.orm import relationship

from backbone.infrastructure.postgres_connection import BaseEntity
from ieee.domain.entities.article_author_association import file_author_association


class AuthorEntity(BaseEntity):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    uuid = Column(Uuid, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    affiliation = Column(String(255))
    authors_id = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    articles = relationship("ArticleEntity", secondary=file_author_association, back_populates="authors")
