import dataclasses
from typing import Optional, List
from uuid import UUID


@dataclasses.dataclass
class DetailKeyword:
    type: Optional[str]
    keyword: Optional[str]


@dataclasses.dataclass
class DetailAuthors:
    id: Optional[int]
    firstName: Optional[str]
    lastName: Optional[str]
    affiliation: Optional[str]
    bio: Optional[str]
    orcid: Optional[str]


@dataclasses.dataclass
class DetailIssn:
    article_id: Optional[UUID]
    format: Optional[str]
    value: Optional[str]


@dataclasses.dataclass
class ArticlePageDTO:
    uuid: Optional[UUID]
    link_article: Optional[str]
    content_of_article: Optional[str]
    title: Optional[str]
    publisher: Optional[str]
    abstract: Optional[str]
    published_in: Optional[str]
    date_of_conference: Optional[str]
    doi: Optional[str]
    insert_date: Optional[str]
    conf_loc: Optional[str]
    publication_date: Optional[str]
    start_page: Optional[int]
    end_page: Optional[int]
    article_id: Optional[int]
    path: Optional[str] = dataclasses.field(default_factory="")
    authors: List[DetailAuthors] = dataclasses.field(default_factory=[])
    issn: List[DetailIssn] = dataclasses.field(default_factory=[])
    keywords: List[DetailKeyword] = dataclasses.field(default_factory=[])


class ArticleDTO:
    uuid: Optional[UUID]
    link_article: Optional[str]
    content_of_article: Optional[str]
    title: Optional[str]
    publisher: Optional[str]
    abstract: Optional[str]
    published_in: Optional[str]
    date_of_conference: Optional[str]
    doi: Optional[str]
    insert_date: Optional[str]
    conf_loc: Optional[str]
    publication_date: Optional[str]
    start_page: Optional[int]
    end_page: Optional[int]
    article_id: Optional[int]

    @classmethod
    def add(cls, detail_page: ArticlePageDTO, authors: List):
        article_data = ArticleDTO()
        article_data.uuid = detail_page.uuid
        article_data.link_article = detail_page.link_article
        article_data.content_of_article = detail_page.content_of_article
        article_data.title = detail_page.title
        article_data.publisher = detail_page.publisher
        article_data.abstract = detail_page.abstract
        article_data.published_in = detail_page.published_in
        article_data.date_of_conference = detail_page.date_of_conference
        article_data.doi = detail_page.doi
        article_data.insert_date = detail_page.insert_date
        article_data.conf_loc = detail_page.conf_loc
        article_data.publication_date = detail_page.publication_date
        article_data.start_page = detail_page.start_page
        article_data.end_page = detail_page.end_page
        article_data.article_id = detail_page.article_id
        return article_data
