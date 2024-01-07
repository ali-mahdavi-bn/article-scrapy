from typing import List

from articles.domain.entities import ArticleAuthorAssociation
from articles.domain.entities.issn import Issn
from articles.spider.dto.article import ArticlePageDTO
from unit_of_work import UnitOfWork


def make_group_article_author(authors, detail_page_ieee: ArticlePageDTO) -> List[Issn]:

    issn_list = []
    if authors:
        for author in authors:
            author_entity = create_article_author_entity(author, detail_page_ieee.uuid)
            issn_list.append(author_entity)

    return issn_list


def create_article_author_entity(author, article_id):
    article_author_entity = ArticleAuthorAssociation.create(article_id=article_id, author_id=author.uuid)
    return article_author_entity
