from sqlalchemy import Table, Integer, ForeignKey, Column

from backbone.infrastructure.postgres_connection import BaseEntity

file_author_association = Table('article_author_association', BaseEntity.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('article_id', Integer, ForeignKey('articles.id')),
                                Column('author_id', Integer, ForeignKey('authors.id'))
                                )

# class file_author_association(baseEntity):
#     __tablename__ = 'file_author_association'
#
#     id = Column(Integer, primary_key=True)
#     file_id = Column(Uuid, ForeignKey('files.uuid'))
#     author_id = Column(Integer, ForeignKey('authors.id'))
#
#     files = relationship("FileEntity", back_populates="file_author_association")
#     authors = relationship("AuthorEntity", back_populates="file_author_association")
