from typing import List

from ieee.domain.detail import DetailPage
from ieee.domain.entities import KeywordEntity


def make_list_keyword(detail_page_ieee: DetailPage) -> List[KeywordEntity]:
    keywords = detail_page_ieee.keywords
    article_id = detail_page_ieee.uuid

    return [
        create_keyword_entity(keyword, article_id)
        for keyword in keywords
    ]


def create_keyword_entity(keyword, article_id):
    keyword_entity = KeywordEntity()
    keyword_entity.type = keyword.type
    keyword_entity.keyword = keyword.keyword
    keyword_entity.article_id = article_id
    return keyword_entity
