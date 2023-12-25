from typing import Optional, List
from uuid import UUID

from ieee.domain.detail import DetailPage


class PaperData:
    uuid: UUID
    title: Optional[str]
    article_text: Optional[str]
    link_article: Optional[str]
    displayPublicationTitle: Optional[str]
    abstract: Optional[str]
    publicationDate: Optional[str]
    fundingName: Optional[str]
    confLoc: Optional[str]
    publisher: Optional[str]
    insertDate: Optional[str]
    articleId: Optional[int]
    volume: Optional[int]
    issue: Optional[int]
    authors: Optional[List]

    @classmethod
    def create(cls, detail_page: DetailPage, authors: List):
        paper_data = PaperData()
        paper_data.uuid = detail_page.uuid
        paper_data.articleId = detail_page.articleId
        paper_data.link_article = detail_page.link_article
        paper_data.title = detail_page.title
        paper_data.article_text = detail_page.article_text
        paper_data.displayPublicationTitle = detail_page.displayPublicationTitle
        paper_data.abstract = detail_page.abstract
        paper_data.publicationDate = detail_page.publicationDate
        paper_data.fundingName = detail_page.fundingName
        paper_data.confLoc = detail_page.confLoc
        paper_data.volume = detail_page.volume
        paper_data.issue = detail_page.issue
        paper_data.authors = authors
        return paper_data
