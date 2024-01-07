from typing import List

from articles.domain.entities.keyword import Keyword
from articles.spider.dto.article import ArticlePageDTO


def make_group_keyword(detail_page_ieee: ArticlePageDTO) -> List[Keyword]:
    keywords = detail_page_ieee.keywords
    article_id = detail_page_ieee.uuid

    return [
        create_keyword_entity(keyword, article_id)
        for keyword in keywords
    ]


def create_keyword_entity(keyword, article_id):
    keyword_entity = Keyword()
    keyword_entity.type = keyword.type
    keyword_entity.keyword = keyword.keyword
    keyword_entity.article_id = article_id
    return keyword_entity
