from typing import List

from ieee.domain.detail import DetailPage
from ieee.domain.entities import IssnEntity


def make_list_issn(detail_page_ieee: DetailPage) -> List[IssnEntity]:
    issn_list = []
    issn_data = detail_page_ieee.issn
    if issn_data:
        for data in issn_data:
            issn_entity = create_issn_entity(data)
            issn_list.append(issn_entity)

    return issn_list


def create_issn_entity(data):
    issn_entity = IssnEntity()
    issn_entity.format = data.format
    issn_entity.value = data.value
    issn_entity.articles_id = data.article_id
    return issn_entity
