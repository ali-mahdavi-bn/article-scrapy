from sqlalchemy import Integer, Column, String, DateTime, func, Text, Uuid
from sqlalchemy.orm import relationship

from backbone.infrastructure.postgres_connection import BaseEntity
from ieee.domain.command import PaperData
from ieee.domain.entities.article_author_association import file_author_association


class ArticleEntity(BaseEntity):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    uuid = Column(Uuid, unique=True)
    link_article = Column(String, nullable=False)
    format = Column(String(100))
    article_text = Column(Text)
    displayPublicationTitle = Column(String(255))
    abstract = Column(Text)
    title = Column(String(255))
    doi = Column(String(255))
    publication_date = Column(String(100))
    funding_name = Column(String(100))
    conf_loc = Column(String(100))
    article_id = Column(Integer)
    volume = Column(Integer)
    issue = Column(Integer)
    publisher = Column(String(255))
    insert_date = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    authors = relationship("AuthorEntity", secondary=file_author_association, back_populates="articles")
    issn = relationship("IssnEntity", back_populates="articles")
    keywords = relationship("KeywordEntity", back_populates="articles")

    @classmethod
    def create(self, data: PaperData, format=None):
        article = ArticleEntity()
        article.uuid = data.uuid
        article.format = format
        article.title = data.title
        article.link_article = data.link_article
        article.article_text = data.article_text
        article.displayPublicationTitle = data.displayPublicationTitle
        article.abstract = data.abstract
        article.publicationDate = data.publicationDate
        article.fundingName = data.fundingName
        article.confLoc = data.confLoc
        article.articleId = data.articleId
        article.volume = data.volume
        article.issue = data.issue
        for author in data.authors:
            article.authors.append(author)

        return article

    def update(self, data: PaperData, article_text, format=None):
        self.link_article = data.link_article or self.link_article
        self.format = format or self.format
        self.title = data.title or self.title
        self.article_text = article_text
        self.displayDocTitle = data.displayDocTitle or self.displayDocTitle
        self.displayPublicationTitle = data.displayPublicationTitle or self.displayPublicationTitle
        self.abstract = data.abstract or self.abstract
        self.publicationDate = data.publicationDate or self.publicationDate
        self.fundingName = data.fundingName or self.fundingName
        self.confLoc = data.confLoc or self.confLoc
        self.volume = data.volume or self.volume
        self.issue = data.issue or self.issue
        self.publisher = data.publisher or self.publisher
        self.insertDate = data.insertDate or self.insertDate

# class FileEntity(baseEntity):
#     __tablename__ = 'files'
#
#     id = Column(Integer, primary_key=True)
#     uuid = Column(Uuid, unique=True)
#     format = Column(String(100))
#     file_text = Column(Text)
#     displayDocTitle = Column(String(255))
#     displayPublicationTitle = Column(String(255))
#     abstract = Column(Text)
#     title = Column(String(255))
#     publicationDate = Column(String(100))
#     fundingName = Column(String(100))
#     confLoc = Column(String(100))
#     articleId = Column(Integer)
#     volume = Column(Integer)
#     issue = Column(Integer)
#     publisher = Column(String(255))
#     insertDate = Column(String(255))
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
#
#     authors = relationship("AuthorEntity", secondary=file_author_association, back_populates="files")
#     issn = relationship("IssnEntity", back_populates="files")
#     keywords = relationship("KeywordEntity", back_populates="files")
#
#     @classmethod
#     def create(self, file_detail: CreateFile, authors, format):
#         file = FileEntity()
#         file.format = format
#         file.uuid = file_detail.uuid
#         file.title = file_detail.title
#         file.file_text = file_detail.file_text
#         file.displayDocTitle = file_detail.displayDocTitle
#         file.displayPublicationTitle = file_detail.displayPublicationTitle
#         file.abstract = file_detail.abstract
#         file.publicationDate = file_detail.publicationDate
#         file.fundingName = file_detail.fundingName
#         file.confLoc = file_detail.confLoc
#         file.articleId = file_detail.articleId
#         file.volume = file_detail.volume
#         file.issue = file_detail.issue
#         return file
