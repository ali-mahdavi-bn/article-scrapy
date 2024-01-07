from typing import List

from articles.domain.entities.issn import Issn
from articles.spider.dto.article import ArticlePageDTO


def make_group_issn(detail_page_ieee: ArticlePageDTO) -> List[Issn]:
    issn_list = []
    issn_data = detail_page_ieee.issn
    if issn_data:
        for data in issn_data:
            issn_entity = create_issn_entity(data)
            issn_list.append(issn_entity)

    return issn_list


def create_issn_entity(data):
    issn_entity = Issn()
    issn_entity.format = data.format
    issn_entity.value = data.value
    issn_entity.articles_id = data.article_id
    return issn_entity
