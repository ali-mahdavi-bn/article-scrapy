from sqlalchemy import Table, Integer, Column, String, DateTime, func, ForeignKey, Uuid
from sqlalchemy.orm import relationship

from backbone.infrastructure.postgres_connection import BaseEntity


class KeywordEntity(BaseEntity):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    keyword = Column(String(100))
    article_id = Column(Uuid, ForeignKey('articles.uuid'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    articles = relationship("ArticleEntity", back_populates="keywords")
