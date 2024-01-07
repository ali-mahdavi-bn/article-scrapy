from datetime import datetime
from uuid import UUID

from articles.spider.dto.article import ArticleDTO
from backbone.adapter.abstract_entity import BaseEntity


class Article(BaseEntity):
    id: int
    uuid: UUID
    link_article: str
    content_of_article: str
    title: str
    publisher: str
    abstract: str
    published_in: str
    date_of_conference: str
    doi: str
    insert_date: str
    conf_loc: str
    publication_date: str
    start_page: int
    end_page: int
    article_id: int
    language_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, data: ArticleDTO, format=None):
        article = Article()
        article.language_id=1
        article.format = format
        article.uuid = data.uuid
        article.link_article = data.link_article
        article.content_of_article = data.content_of_article
        article.title = data.title
        article.publisher = data.publisher
        article.abstract = data.abstract
        article.published_in = data.published_in
        article.date_of_conference = data.date_of_conference
        article.doi = data.doi
        article.insert_date = data.insert_date
        article.conf_loc = data.conf_loc
        article.publication_date = data.publication_date
        article.start_page = data.start_page
        article.end_page = data.end_page
        article.article_id = data.article_id
        return article

    def update(self, data: ArticleDTO, format=None):
        self.format = format or self.format
        self.link_article = data.link_article or self.link_article
        self.content_of_article = data.content_of_article or self.content_of_article
        self.title = data.title or self.title
        self.publisher = data.publisher or self.publisher
        self.abstract = data.abstract or self.abstract
        self.published_in = data.published_in or self.published_in
        self.date_of_conference = data.date_of_conference or self.date_of_conference
        self.doi = data.doi or self.doi
        self.insert_date = data.insert_date or self.insert_date
        self.conf_loc = data.conf_loc or self.conf_loc
        self.publication_date = data.publication_date or self.publication_date
        self.start_page = data.start_page or self.start_page
        self.end_page = data.end_page or self.end_page
        self.article_id = data.article_id or self.article_id

    def update_article_text(self, content_of_article: str = ""):
        self.content_of_article = content_of_article
